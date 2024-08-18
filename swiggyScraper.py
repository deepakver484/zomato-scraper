from selenium.webdriver.common.by import By
from seleniumwire2 import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from utils import setup_logger, take_screenshot, try_element
from time import sleep 
import re
from urllib.parse import urlparse, parse_qs, unquote


class swiggyScraper:
    def __init__(self, headless = True):
        self.headless = headless
        self.driver = self._setup_driver()
        self.logger = setup_logger()
        self.url = 'https://www.swiggy.com/'
        self.base_url = 'https://swiggy.com/restaurants/'


    '''
    this function will initiate webdriver.chrome and return driver
    '''
    def _setup_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless=new")  # Run in headless mode
            chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
        return webdriver.Chrome(options=chrome_options)
    

    '''
    this will open website url and wait 5 sec
    params:- 
    url - website url you want to open
    '''
    def open_website(self, url):
        self.driver.get(url)
        self.logger.info(f"Opened website: {url}")
        sleep(10)

    '''
    this function will get the recommended location found on the swiggy website
    params:-
    location - location you are searching on the search box of swiggy
    return - dictionary having all the recommended location
    '''
    def get_location(self, location):
        # opening website
        self.open_website(url = self.url)
        # finding the tab for search location and click on it
        self.driver.find_element(By.XPATH, '//span[contains(text(),"Other")]').click()
        # getting the input button
        search_button = self.driver.find_element(By.TAG_NAME, 'input')
        # feeding the location on the input button
        search_button.send_keys(location)
        sleep(1)
        # getting all the recommendation location elements
        location_elements = self.driver.find_elements(By.XPATH, '//div[contains(@class,"icon-location")]/..')
        # getting all the text from the location elements and converting it to the dictionary
        location_dict = {location.text: location for location in location_elements}
        return location_dict
    

    '''
    this function will help us to select one of the location on the swiggy website from dictionary location
    params- 
    location_dict - dictonary contains all the recommended location
    location_name - selected location_name
    '''
    def select_location(self, location_dict,location_name):
        #click on the locatin_name on the swiggy website
        location_dict[location_name].click()
        self.logger.info(f"Selected location: '{location_name}'")
        sleep(5)


    '''
    this will get the slug from the links getting from the network tab
    and return list os slugs.     
    '''
    def get_slug(self):
        # List to store the extracted restaurant slugs
        restaurant_slugs = []

        # Iterate through all network requests captured by Selenium-Wire
        for request in self.driver.requests:
            if request.response:
                # Check if the URL contains the word "restaurants"
                if re.search(r'restaurants', request.url, re.IGNORECASE):

                    # Attempt to extract the slug directly from the URL
                    match = re.search(r'restaurants\/([\w-]+)', request.url)
                    if match:
                        restaurant_slug = match.group(1)
                        restaurant_slugs.append(restaurant_slug)
                    else:
                        print("No restaurant slug found directly in the URL.")

                    # Parse the URL to decode the query string
                    parsed_url = urlparse(request.url)
                    query_params = parse_qs(parsed_url.query)

                    # If 'cx' parameter exists, try extracting the slug from there
                    cx_value = query_params.get('cx', [None])[0]
                    if cx_value:
                        # Decode the cx_value from URL encoding
                        cx_value_decoded = unquote(cx_value)

                        # Try to extract the restaurant link from the cx JSON
                        match = re.search(r'"link":"https:\/\/www.swiggy.com\/restaurants\/([\w-]+)"', cx_value_decoded)
                        if match:
                            restaurant_slug = match.group(1)
                            restaurant_slugs.append(restaurant_slug)
                            print(f"Extracted slug from cx: {restaurant_slug}")
                        else:
                            print("No restaurant slug found in the cx parameter.")
                    else:
                        print("No 'cx' parameter found in the URL.")

        # Print all collected restaurant slugs
        print("Collected restaurant slugs:", restaurant_slugs)
        return restaurant_slugs


    '''
    get_restaurant_urls method to get the links of each restaurant 
    params :-
    num :- number of restaurants data you want to scrape
    return :- list of num of number of restaurant urls.'''
    def get_restaurant_urls(self, num):
        try:
            take_screenshot(self.driver, self.logger, "initial_load_swiggy.png")
            # Initialize the list and set up an explicit wait
            li = []
            wait = WebDriverWait(self.driver, 10)  # Adjust the timeout as needed

            while True:
                if len(li) == 0:
                    # Wait for the elements to be present
                    wait.until(EC.presence_of_all_elements_located((By.XPATH, '//div[contains(@class,"sw-restaurant-card-subtext-container")]/../..')))
                    li = self.driver.find_elements(By.XPATH, '//div[contains(@class,"sw-restaurant-card-subtext-container")]/../..')
                
                if len(li) == 0:
                    # If no elements found, break the loop
                    self.logger.warning("No restaurant cards found.")
                    break
                
                element = li[-1]
                self.driver.execute_script("arguments[0].scrollIntoView();", element)
                
                # Use an explicit wait to ensure new elements are loaded
                sleep(5)
                # finding the resturant_cards anchor element
                li = self.driver.find_elements(By.XPATH, '//div[contains(@class,"sw-restaurant-card-subtext-container")]/../..')
                self.logger.info(f"{len(li)} number of restaurants cards found")

            # Get URLs
                slug_list = self.get_slug()
                restaurant_urls = [self.base_url+link for link in slug_list if link != 'list']
                if len(restaurant_urls) >= num:
                    break
            return restaurant_urls[:num]
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return []


    '''
    this will get the head_info like - name, ratings, category, offers for a restaurant
    return:- return dictionary of data contains all above data
    '''
    def get_head_info(self):
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.presence_of_all_elements_located((By.TAG_NAME, 'h1')))
        # getting name of the restaurant
        name = try_element('tag_name', 'h1', driver = self.driver, logger= self.logger).text
        box_div = try_element('xpath', '//div[contains(text(),"for")]/../..', driver = self.driver , logger = self.logger)
        # getting overall ratings and votes of the restaurant
        ratings = try_element('xpath','//div[contains(text(), "for")]/..', driver=box_div, logger=self.logger).text
        # getting the categories of the restaruant
        category = try_element('tag_name', 'a', driver =box_div, logger= self.logger, element=False)
        categories = [a.text for a in category]
        # getting offers of the restaurant
        offers= try_element('xpath', '//h2[contains(text(),"Deals for you")]/../../..', driver = self.driver, logger=self.logger).text.split('\n')
        return {
            "name": name,
            "ratings": ratings,
            "categories" : categories,
            "offers": offers
        }


    '''
    this will extract dishcontent and ratingscontent from the dish_element
    params - selenium element fo dish_element
    return - dictionary containing dish_content and ratings_content
    '''
    def extract_dish(self, dish_element):
        # getting the dish_content having name, veg_type, price, description
        dish_content = try_element('tag_name', 'p', driver = dish_element, logger= self.logger).text
        # getting the reatings content having ratings, votes
        ratings_content = try_element('xpath', './/*[local-name()="rect"]/../../..', driver=dish_element, logger=self.logger).text
        return {
            "dish_content": dish_content,
            "ratings_content": ratings_content
        }


    '''
    this will process dish_elements using for loop and apply extract_dish
    params:- 
    dish_elements - selenium elements of containing all the elements having dish elements
    return :- return the data having dictionary of dish
    '''
    def process_dish_element(self, dish_elements):
        data = []
        # run for loop for each dish element fron dish elements
        for dish in dish_elements:
            # extracting dish data from dish element
            dict_dish = self.extract_dish(dish)
            # appending dict_dish into the data
            data.append(dict_dish)
        return data


    '''
    this function will the get all the data for a perticular restaurant
    params:- 
    url - url of the restaurant
    return - dictionary having all the data of the restaurant
    '''
    def get_restaurant_data(self, url):
        # opening restaurant url
        self.open_website(url)
        # getting head info of the restaurant
        data = self.get_head_info()
        # getting all the dish elements from the restaurant page
        dish_elements= try_element('xpath', '//div[@data-testid="normal-dish-item"]', driver=self.driver, logger= self.driver, element =False)
        # processing all the dish elements to get the data form it
        data["dish_data"] = self.process_dish_element(dish_elements)
        # returning data
        return data
    
    