from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urlparse, parse_qs
from time import sleep
import  logging


# Creating a Class RestaurantScraper for all the scraping Functionality
class RestaurantScraper:
    def __init__(self, headless = True):
        self.headless = headless
        self.driver = self._setup_driver()
        self.logger = self._setup_logger()


    def _setup_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless=new")  # Run in headless mode
            chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
        return webdriver.Chrome(options=chrome_options)


    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        return logger


    def _take_screenshot(self, filename):
        """Take a screenshot and save it to the specified file."""
        self.driver.save_screenshot(filename)
        self.logger.info(f"Screenshot saved as {filename}")


    '''
    get_restaurant_urls method to get the links of each restaurant 
    params :-
    link :- link of the zomato with the area 
    num :- number of restaurants data you want to scrape'''
    def get_restaurant_urls(self, link, num):
        try:
            self.logger.info(f"Fetching restaurant URLs from {link}")
            self.driver.get(link)
            sleep(10)

            self._take_screenshot("initial_load.png")
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
    try_element function - this function handles the error (elements not found)
    params:-
    tay_type - it is the type of element I am searching on it
    tag_path - is is either class ,tagname or xpath
    element - bool (either finding (element :- True) or (elements :- False))
    '''
    def try_element(self, tag_type, tag_path, driver, element = True):
        result = None
        
        if element:
            try:
                by_type = getattr(By, tag_type.upper())
                result = driver.find_element(by_type, tag_path)
                self.logger.info(f"Element found: {result}")
            except NoSuchElementException:
                result = 'not found'
                self.logger.warning(f"Element not found with {tag_type}='{tag_path}'")

        else:
            try:
                by_type = getattr(By, tag_type.upper())
                result = driver.find_elements(by_type, tag_path)
                self.logger.info(f"Elements found: {len(result)}")
            except NoSuchElementException:
                result = 'not found'
                self.logger.warning(f"Elements not found with {tag_type}='{tag_path}'")

        return result
  

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


    def get_head_info(self):
        head_div = self.try_element('xpath', '//div[contains(text(),"Ratings")]/../../../../..', driver=self.driver)
        name_element = self.try_element('TAG_NAME', 'h1', driver= head_div)
        name = name_element.text

        print(name)
        rating_element = self.try_element('XPATH', '//div[contains(text(),"Ratings")]/../../..', driver= self.driver)
        ratings = rating_element.text.split('\n')
        print(ratings)
        category_element = self.try_element('XPATH', '//div[contains(text(),"Ratings")]/../../../../../../section[1]/div', driver=self.driver)
        category = category_element.text.split(', ')
        print(category)
        location_element = self.try_element('XPATH','//div[contains(text(),"Ratings")]/../../../../../../section[1]/a', driver = self.driver)
        location = location_element.text.split()
        print(location)
        time_element = self.try_element('XPATH', '//div[contains(text(),"Ratings")]/../../../../../../section[2]', driver = self.driver)
        time = time_element.text
        print(time)
        destination_element = self.try_element('XPATH', '//span[contains(text(),"Direction")]/../..', driver = self.driver)
        destination_url = destination_element.get_attribute('href')
        coordinates = self.get_location(destination_url)
        print(coordinates)


        # driver.find_element(By.XPATH, '//span[contains(text(),"Direction")]/../..').get_attribute('href')
        #driver.find_element(By.XPATH, '//div[contains(text(),"Ratings")]/../../../../../../section[2]').text
        # driver.find_element(By.XPATH, '//div[contains(text(),"Ratings")]/../../../../../../section[1]/a').text
        # driver.find_element(By.XPATH, '//div[contains(text(),"Ratings")]/../../../../../../section[1]/div').text
        # driver.find_element(By.XPATH, '//div[contains(text(),"Ratings")]/../../..').text.split('\n')
        # name = head_div.find_element(By.TAG_NAME, 'h1').text
        # head_div = self.driver.find_element(By.XPATH, '//div[contains(text(),"Ratings")]/../../../../..')


    def get_restaurant_data(self, restaurant_link):
        try:
            self.logger.info(f"Fetching restaurant URL from {restaurant_link}")
            self.driver.get(restaurant_link)
            data = self.get_head_info()
            # order_section = self.try_element('xpath', '//h2[contains(text(),"Order Online")]/../../../section', element=False)
            # order_section = order_section[1:]


            # order_section = driver.find_elements(By.XPATH, '//h2[contains(text(),"Order Online")]/../../../section')[1:]
            # data = {

            # }

            return data

        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return {

            }


    def close_driver(self):
        self.driver.quit()  # Close the WebDriver when done
