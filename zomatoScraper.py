from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from urllib.parse import urlparse, parse_qs
from time import sleep
from utils import setup_logger, take_screenshot, try_element


# Creating a Class RestaurantScraper for all the scraping Functionality
class RestaurantScraper:
    def __init__(self, headless = True):
        self.headless = headless
        self.driver = self._setup_driver()
        self.logger = setup_logger()


    def _setup_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless=new")  # Run in headless mode
            chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
        return webdriver.Chrome(options=chrome_options)

    '''
    get_restaurant_urls method to get the links of each restaurant 
    params :-
    link :- link of the zomato with the area 
    num :- number of restaurants data you want to scrape'''
    def get_restaurant_urls(self, link, num):
        try:
            self.logger.info(f"Fetching restaurant URLs from {link}")
            self.driver.get(link)
            self.driver.implicitly_wait(10)
            sleep(5)

            take_screenshot(self.driver, self.logger, "initial_load.png")
            # Initialize the list and set up an explicit wait
            li = []
            wait = WebDriverWait(self.driver, 10)  # Adjust the timeout as needed

            while True:
                if len(li) == 0:
                    # Wait for the elements to be present
                    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//img[@alt="Restaurant Card"]/../..')))
                    li = self.driver.find_elements(By.XPATH, '//img[@alt="Restaurant Card"]/../..')
                
                if len(li) == 0:
                    # If no elements found, break the loop
                    self.logger.warning("No restaurant cards found.")
                    break
                
                element = li[-1]
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                
                # Use an explicit wait to ensure new elements are loaded
                sleep(5)
                # finding the resturant_cards anchor element
                li = self.driver.find_elements(By.XPATH, '//img[@alt="Restaurant Card"]/../..')
                self.logger.info(f"{len(li)} number of restaurants cards found")
                
                if len(li) >= num:
                    break

            # Get URLs
            restaurant_urls = [link.get_attribute('href') for link in li[:num]]
            self.logger.info(f"Successfully fetched {len(restaurant_urls)} restaurant URLs")
            return restaurant_urls
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return []
  

    '''
    get_location function to extract the latitude and longitude from the destination_url
    params :-
    destination_url -> it's the url of location which consists latitude and longitude
    '''
    def get_location(self, destination_url):
        parsed_url = urlparse(destination_url)
        query_params = parse_qs(parsed_url.query)

        # Extract the 'destination' parameter
        destination = query_params.get('destination', [None])[0]

        if destination:
            # Split the 'destination' parameter to get latitude and longitude
            latitude, longitude = destination.split(',')
            self.logger.info(f"Latitude: {latitude}")
            self.logger.info(f"Longitude: {longitude}")
            return {
                'latitude' : latitude, 
                'longitude' : longitude
                }
        else:
            self.logger.warning("No destination parameter found in the URL")
            return {
                'latitude' : 'not available', 
                'longitude' : 'not available'
                }


    '''
    get_dynamic_tooltip_text - to get the from the dynamic tooltip element
    params: -
    tooltip_xpath - xpath of the dynamic tool_tip
    text_element - xpath of the tooltip text containing element 
    '''
    def get_dynamic_tooltip_text(self, tooltip_xpath, text_element):
        #finding tool tip element
        tooltip_element = try_element('xpath', tooltip_xpath, driver= self.driver, logger=self.logger)

        action = ActionChains(self.driver)
        #moving cursor to hover over the tooltip div to activate the script
        action.move_to_element(tooltip_element).perform()
            
        # Capture the tooltip's text from the displayed elements
        tooltip_text = try_element('xpath', text_element, driver= self.driver, logger=self.logger).text
        return tooltip_text


    '''
    get_head_info - it will extract data of head element like name, ratings, category, location, time , coordinates
    '''
    def get_head_info(self):
        head_div = try_element('xpath', '//div[contains(text(),"Ratings")]/../../../../..', driver = self.driver, logger=self.logger)
        
        # finding name of the restaurant
        name_element = try_element('TAG_NAME', 'h1', driver= head_div, logger=self.logger)
        name = name_element.text
        
        # finding the resaurants ratings
        rating_element = try_element('XPATH', '//div[contains(text(),"Ratings")]/../../..', driver = self.driver, logger=self.logger)
        rating = rating_element.text.split('\n')
        
        # finding the categories restaurant served
        category_element = try_element('XPATH', '//div[contains(text(),"Ratings")]/../../../../../../section[1]/div', driver = self.driver, logger=self.logger)
        category = category_element.text.split(', ')
        
        #finding the location of the restaurant
        location_element = try_element('XPATH','//div[contains(text(),"Ratings")]/../../../../../../section[1]/a', driver = self.driver, logger=self.logger)
        location = location_element.text.split(', ')
        
        # finding the opening and closing time
        tooltip_xpath = '//div[@role ="tooltip"]'
        text_element = '//span[@role="tooltip"]'
        time = self.get_dynamic_tooltip_text(tooltip_xpath=tooltip_xpath, text_element=text_element)
        
        #findnig the cordinates of the restaurant
        destination_element = try_element('XPATH', '//span[contains(text(),"Direction")]/../..', driver= self.driver, logger=self.logger)
        destination_url = destination_element.get_attribute('href')
        coordinates = self.get_location(destination_url)

        data = {
            "name" : name,
            "rating" : rating,
            "category" : category,
            "location" : location,
            "time" : time,
            "coordinates" : coordinates
        }
        return data

    
    '''
    extract_order_sections - this function will get all the dish card elements from the restaurant page
    params: -
    no parameter required
    '''
    def extract_order_sections(self):

        # Find the order sections after the first one
        order_section = try_element('xpath', '//h2[contains(text(),"Order Online")]/../../../section', driver = self.driver, element=False, logger=self.logger)
        order_section = order_section[1:]  # Skip the first section due not having the relevent content
        
        order_div = []
        # Loop through each section and find div elements with text
        for sec in order_section:
            divs = try_element('xpath', 'div', driver = sec, element=False, logger=self.logger)
            self.logger.info(f"Found {len(divs)} div elements in section.")
            for div in divs:
                if div.text:
                    order_div.append(div)
                    self.logger.debug(f"Appended div with text: {div.text}")

        dish_card = []
        # Loop through each order div and find inner div elements
        for div in order_div:
            dish_card += try_element('xpath', 'div', driver = div, element=False, logger=self.logger)
            self.logger.info(f"Extracted {len(dish_card)} dish cards so far.")

        return dish_card


    '''
    process_dish_card - this function will get the dish ratings
    params - 
    dish_card - element of the dish_card
    '''
    def ratings_dish_card(self, dish_card):
        counter = 0
        i_tags = try_element('tag_name', 'i', element=False, driver = dish_card, logger=self.logger)
        
        # Check the color attribute of the first element to judge the dish either veg or nonveg
        color = i_tags[0].get_attribute('color')
        if color == '#3AB757':
            dish_type = 'veg'
        elif color == '#BF4C43':
            dish_type = 'non-veg'
        else:
            self.logger.warning(f'Unknown dish with color code: {color}')

        if len(i_tags) == 1:
            return counter, dish_type
        
        # Process remaining elements
        for i_tag in i_tags[1:]:
            i_element = try_element('tag_name', 'title', driver = i_tag, logger=self.logger)
            if i_element.text != 'Not found':
                # increase the counter rating
                counter += 1
            else:
                # getting the decimal of the rating
                last = try_element('xpath', './/*[local-name()="stop" and @stop-color="#F3C117"]', element=False,driver= i_tag, logger=self.logger)
                if len(last) == 0:
                    break
                else:
                    last = last[1]
                counter += int(last.get_attribute('offset').replace('%', '')) * 0.01
                break
        return counter, dish_type   


    '''
    extract_dish_card - this function will get the dish info
    params:-
    dish_card - dish_card Web element
    '''
    def extract_dish_card(self, dish_card):
        # Extract the dish name
        dish_name = try_element('tag_name', 'H4', driver=dish_card, logger=self.logger).text
            
        # Extract the number of votes
        dish_votes = try_element('xpath', './/span[contains(text(), "votes")]', driver = dish_card, logger=self.logger).text
            
        # Extract the dish price
        dish_price = try_element('xpath', './/span[contains(text(), "₹")]', driver = dish_card, logger=self.logger).text

        # Check if the "read more" button for description exists and click it if found
        dish_description_read_more = try_element('xpath', './/span[contains(text(), "read more")]', driver = dish_card, logger=self.logger)
        if dish_description_read_more.text != 'Not found':
            dish_description_read_more.click()
            self.logger.info("Clicked on 'read more' for dish description.")

        # Extract the dish description
        dish_description = try_element('tag_name', 'p', driver = dish_card, logger=self.logger).text

        #Extract the rating
        rating, dish_type = self.ratings_dish_card(dish_card)

        # Return the extracted information as a dictionary
        dish_info = {
                "name": dish_name,
                "votes": dish_votes,
                "price": dish_price,
                "description": dish_description,
                "rating" : rating,
                "dish_type" : dish_type
            }

        return dish_info


    '''
    get_restaurant_data - this function will scrap all the info of a restaurant
    params :-
    restaurant_link - link of the restaurant
    '''
    def get_restaurant_data(self, restaurant_link):

        try:
            self.logger.info(f"Fetching restaurant data from URL {restaurant_link}")

            # getting the restaurant link
            self.driver.get(restaurant_link)
            sleep(10)
            # calling the get_head_info function to get all the info of the restaurant's head
            data = self.get_head_info()

            # calling the extract_order_sectionos function to get all the dish_section elements
            dish_section = self.extract_order_sections()
            dish_data  = []
            for dish in dish_section:
                #calling extract_dish_card function to get teh dish elements from the dish_section
                dish_data.append(self.extract_dish_card(dish))

            data['dish_data'] = dish_data

            return data

        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return {

            }


    def close_driver(self):
        self.driver.quit()  # Close the WebDriver when done
