from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import  logging

# Creating a Class RestaurantScraper for all the scraping Functionality
class RestaurantScraper:
    def __init__(self, headless=True):
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


    # get_restaurant_urls method to get the links of each restaurant 
    #params :-
    # link :- link of the zomato with the area 
    # num :- number of restaurants data you want to scrape
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
                li = self.driver.find_elements(By.XPATH, '//img[@alt="Restaurant Card"]/../..')
                print(len(li))
                
                if len(li) >= num:
                    break

            # Get URLs
            restaurant_urls = [link.get_attribute('href') for link in li[:num]]
            self.logger.info(f"Successfully fetched {len(restaurant_urls)} restaurant URLs")
            return restaurant_urls
        except Exception as e:
            self.logger.error(f"An error occurred: {str(e)}")
            return []
        

    def close_driver(self):
        self.driver.quit()  # Close the WebDriver when done
