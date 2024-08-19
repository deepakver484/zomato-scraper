# ZOMATO SCRAPER

## Objective -

The primary objective of this project is to develop an automated data pipeline that scrapes restaurant information from both Zomato and Swiggy, processes and cleans the scraped data, and outputs it in a structured format. This pipeline is designed to be flexible, allowing users to specify the URLs of Zomato and Swiggy restaurant listings and the number of restaurants to scrape. The cleaned data is then stored in a CSV file, making it ready for further analysis or reporting. Additionally, a Streamlit app will be developed to provide an interactive interface, allowing users to seamlessly interact with both scraping scripts.

## Website Selection - 

I chose to scrape Zomato and Swiggy due to their rich and diverse datasets, which offer valuable insights into restaurants, food trends, and customer preferences. Both platforms present unique challenges in data extraction, with Zomato's dynamic HTML content, including lazily loaded elements, and Swiggy's complex web structures. This complexity is particularly evident in dynamic elements like tooltips within SVG elements on Zomato, and in Swiggy's intricate network requests and data retrieval processes, which require advanced handling to ensure accurate data capture. Despite these challenges, the quality of data available on both Zomato and Swiggy is excellent, making them valuable sources for detailed analysis and insights.

## Tools & Libraries-
- Python
- Selenium
- Streamlit
- Pandas
- Logging
- argparse

## Files Info


| **File Name**                                                                                   | **Description**                                           |
|-------------------------------------------------------------------------------------------------|----------------------------------------------             |
| [**utils.py**](https://github.com/deepakver484/zomato-scraper/blob/main/utils.py)                   | file consist common base functions.       |
| [**zomatomMain.py**](https://github.com/deepakver484/zomato-scraper/blob/main/zomatoMain.py)                           | Main pipeline script for executing tasks in shell mode.   |
| [**requirements.txt**](https://github.com/deepakver484/zomato-scraper/blob/main/requirements.txt)         | Lists Python dependencies for the project.                |
| [**app.py**](https://github.com/deepakver484/zomato-scraper/blob/main/app.py)                             | app.py file consist main streamlit app code.                   |
| [**swiggyScraperApp.py**](https://github.com/deepakver484/zomato-scraper/blob/main/pages/swiggyScraperApp.py)                             | swiggyScraperApp file consist swiggy scraper app code.                   |
| [**zomatoScraperApp.py**](https://github.com/deepakver484/zomato-scraper/blob/main/pages/zomatoScraperApp.py)                             | zomatoScraperApp.py file consist zomato scraper streamlit app code.                   |
| [**zomatoCleaner.py**](https://github.com/deepakver484/zomato-scraper/blob/main/zomatoCleaner.py)                     | file consist cleaning code for zomato.                    |
| [**zomatoScraper.py**](https://github.com/deepakver484/zomato-scraper/blob/main/zomatoScraper.py)         | file consist all the scraping code for zomato.            |
| [**swiggyScraper.py**](https://github.com/deepakver484/zomato-scraper/blob/main/swiggyScraper.py)         | file consist all the scraping code for swiggy.            |
| [**swiggyCleaner.py**](https://github.com/deepakver484/zomato-scraper/blob/main/swiggyCleaner.py)         | file consist all the cleaning code for swiggy.            |
| [**web_links.csv**](https://github.com/deepakver484/zomato-scraper/blob/main/web_links.csv)                   | csv file consist data of restaurant's url.                   |
| [**restaurant_data_uncleaned.csv**](https://github.com/deepakver484/zomato-scraper/blob/main/restaurant_data_uncleaned.csv)                   | csv file consist restaurant's uncleaned data. |
| [**swiggy_restaurant_url.csv**](https://github.com/deepakver484/zomato-scraper/blob/main/swiggy_restaurant_url.csv)                   | csv file consist restaurant's url data swiggy.       |
| [**swiggy_uncleaned_restaurant_data.csv**](https://github.com/deepakver484/zomato-scraper/blob/main/swiggy_uncleaned_restaurant_data.csv)                   | csv file consist restaurant's uncleaned data swiggy.       |
| [**swiggy_cleaned_restaurant_data.csv**](https://github.com/deepakver484/zomato-scraper/blob/main/swiggy_uncleaned_restaurant_data.csv)                   | csv file consist restaurant's cleaned data of swiggy.       |
| [**cleaned_restaurant_data.csv**](https://github.com/deepakver484/zomato-scraper/blob/main/cleaned_restaurant_data.csv)                   | csv file consist restaurant's cleaned data of zomato.       |





## Getting Started

To get a local copy up and running, follow these steps.

## Prerequisites

* Git
* Python (version 3.9 or higher)

## Installation
<details>

1. Clone the repo
    ```sh
    git clone https://github.com/deepakver484/zomato-scraper.git
    ```

2. Change to the directory
    ```sh
    cd zomato-scraper
    ```

3. Create a virtual environment
    ```sh
    python -m venv venv
    ```
4. Activate the virtual environment

    On Windows:
    ```sh
    venv\Scripts\activate
    ```

    On macOS and Linux:
    ```sh
    source venv/bin/activate
    ```

5. Install the dependencies
    ```sh
    pip install -r requirements.txt
   ```
</details> 

## Run Zomato Pipeline

 To run pipeline in background run below given python command
```sh
python zomatoMain.py --url "https://www.zomato.com/ncr/delivery-in-connaught-place" --num 1
```
**url** - you can use any url from the zomato website for online delivery.

**num** - number of restaurants you want to scrap.

## Run Streamlit App
7. To run streamlit app
```sh
streamlit run app.py
```

## Detailed approach for the Project
<details>

## Step Involved in Zomato Scraping  

<details>

1.first step involves data scraping from the zomato .
- I break down this problem into two major parts first scrap the links of restaurant from the main page
- then scrap data of each restaurants
- further break down restaurants data scraping into the below given parts
- first scrap the data of the head element
- include name, address, categories, operational days, opening and closing time, latitude and longitude, delivery ratings and Dining ratings.
  
2.next step involved 
- get the order section 
- then get all the dish card from the order section
  
3.in next step we iterate through each dish card to get the below given data
- name, rating,price, veg type and description

4.this step involved in data cleaning
- Convert dictionary column into multiple simple columns
- Clean Ratings Column
- Clean time columns
  
5.Streamlit App building
   
6.Main Pipeline building

7.Rearrage the code following best practices

</details>

## Step Involved in Swiggy Scraping  

<details>

1.first step involves data scraping from the swiggy .
- I break down this problem into two major parts first scrap the links of restaurant from the main page
- then scrap data of each restaurants
- further break down restaurants data scraping into the below given parts
- first scrap the data of the head element
- include name, categories, offers ratings and votes.
  
2.next step involved 
- get the dish elements 
- then get all the dish element from the dish elements
  
3.in next step we iterate through each dish card to get the below given data
- name, rating, price, veg type and description

4.this step involved in data cleaning
- Convert dictionary column into multiple simple columns
- Clean Ratings Column.
- Clean category Column.
- Clean offer Column.
- Clean dish Info.
- Clean ratings and reviews of dishes.

  
5.Streamlit App building
   
6.Main Pipeline building

7.Rearrage the code following best practices

</details>


## Overview of Utils.py
This file contains common functions used in different files across the project.

<details>

- setting up setup_logger function which will hanlde loginig part of the project
```sh
def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger
```

- Configure the screenshot capture function. This function will take screenshot (usefull for debugging)
  ```sh
    def _take_screenshot(self, filename):
        """Take a screenshot and save it to the specified file."""
        self.driver.save_screenshot(filename)
        self.logger.info(f"Screenshot saved as {filename}")
  ```

- Implement the try_element function.
  function will handle the error while using find element and find elements in selenium
```sh
def try_element(self, tag_type, tag_path, driver=None, element = True):
        result = None
        if driver is None:
            driver = self.driver

        if element:
            try:
                by_type = getattr(By, tag_type.upper())
                result = driver.find_element(by_type, tag_path)
                self.logger.info(f"Element found: {result}")
            except NoSuchElementException:
                result = DummyElement()
                self.logger.warning(f"Element not found with {tag_type}='{tag_path}'")

        else:
            try:
                by_type = getattr(By, tag_type.upper())
                result = driver.find_elements(by_type, tag_path)
                self.logger.info(f"Elements found: {len(result)}")
            except NoSuchElementException:
                result = DummyElement()
                self.logger.warning(f"Elements not found with {tag_type}='{tag_path}'")

        return result
```

- Create and initialize the DummyElement
  this will handle error of using .txt and get_attribute
 ```sh
class DummyElement:
    def __init__(self, text="Not found"):
        self.text = text

    def get_attribute(self, attribute):
        return "Not found"
```
  
</details>    



## Overview Of zomatoScraper.py

<details>
    
- Create and initialize the ZomatoScraper class.
```sh
class RestaurantScraper:
    def __init__(self, headless = True):
        self.headless = headless
        self.driver = self._setup_driver()
        self.logger = setup_logger()
```

- Set up the driver function.
```sh
    def _setup_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless=new")  # Run in headless mode
            chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
        return webdriver.Chrome(options=chrome_options)

```
  
**Scraping Restaurant Links:** Initially, we extract the links to individual restaurants from the main page.
```sh
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
```
- **Scraping Restaurant Data:** Once we have the restaurant links, we proceed to scrape detailed data for each restaurant. This process is further divided into several sub-tasks:
  ```sh
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
  ```

- **Head Element Data:** We start by collecting data from the head element, which includes the restaurant's name, address, categories, operational days, opening and closing times, latitude and longitude, delivery ratings, and dining ratings.
  ```sh
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

  ```
  
  - **Location** get the location from the location href
    ```sh
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
    ```
    
  - **opening and closing time** get the data from the tooltip
    ```sh
    def get_dynamic_tooltip_text(self, tooltip_xpath, text_element):
        #finding tool tip element
        tooltip_element = try_element('xpath', tooltip_xpath, driver= self.driver, logger=self.logger)

        action = ActionChains(self.driver)
        #moving cursor to hover over the tooltip div to activate the script
        action.move_to_element(tooltip_element).perform()
            
        # Capture the tooltip's text from the displayed elements
        tooltip_text = try_element('xpath', text_element, driver= self.driver, logger=self.logger).text
        return tooltip_text
    ```

  - **Order Section:** Next, we scrape the order section of the restaurant page.
  ```sh
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

  ```

  - **Dish Cards:** We then extract all the dish cards from the order section. For each dish card, we gather detailed information including the dish name, rating, price, vegetarian type, and description.
    ```sh
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
    ```

    - **Ratings & veg type of the Dish:** this will get the ratings from the dish card.

```sh
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

```



</details> 

## Overview of swiggyScraper.py

<details>

- **Create and Initialize scraping code**
```sh
class swiggyScraper:
    def __init__(self, headless = True):
        self.headless = headless
        self.driver = self._setup_driver()
        self.logger = setup_logger()
        self.url = 'https://www.swiggy.com/'
        self.base_url = 'https://swiggy.com/restaurants/'
```
    
- **Setup Driver:** this function will handle the driver setup for the scraping.
    ```sh
    def _setup_driver(self):
        chrome_options = Options()
        if self.headless:
            chrome_options.add_argument("--headless=new")  # Run in headless mode
            chrome_options.add_argument("--window-size=1920x1080")
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36")
        return webdriver.Chrome(options=chrome_options)
    ```

- **Open Website:** this function will open a url provided and wait for 5 seconds.
  ```sh
    def open_website(self, url):
        self.driver.get(url)
        self.logger.info(f"Opened website: {url}")
        sleep(10)
  ```
- **Open Location:** this function will return the recommended list of locations as per location search on swiggy.
  ```sh
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
  ```

- **Set location:** this function will set the one of the location from the recommended location.

  ```sh
    def select_location(self, location_dict,location_name):
        #click on the locatin_name on the swiggy website
        location_dict[location_name].click()
        self.logger.info(f"Selected location: '{location_name}'")
        sleep(5)
  ```
- **Get Slug:** this function will get the slug from the scraped link.
  ```sh
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

  ```
- **Get Restaurant URL's:** this function will scrap the n number of restaurant links from the website.
```sh
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
```  

- **Get head Info:** This function will get the head information of the resaurant including (name, ratings, review, offers, categories).
  ```sh
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
  ```

- **Extract Dish:** this will get the data of dish from the dish_element.
    ```sh
    def extract_dish(self, dish_element):
        # getting the dish_content having name, veg_type, price, description
        dish_content = try_element('tag_name', 'p', driver = dish_element, logger= self.logger).text
        # getting the reatings content having ratings, votes
        ratings_content = try_element('xpath', './/*[local-name()="rect"]/../../..', driver=dish_element, logger=self.logger).text
        return {
            "dish_content": dish_content,
            "ratings_content": ratings_content
        }

    ```
- **Process dish element:** this function will process the dish data
  ```sh
    def process_dish_element(self, dish_elements):
        data = []
        # run for loop for each dish element fron dish elements
        for dish in dish_elements:
            # extracting dish data from dish element
            dict_dish = self.extract_dish(dish)
            # appending dict_dish into the data
            data.append(dict_dish)
        return data
  ```
- **Get Restaurant Data:** With the help of above function this function will get the data of the restaurant.
  ```sh
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
  ```
    
</details>

## Overview of data cleaning of Zomato

This section outlines a comprehensive approach for data cleaning. The process includes initializing a class, setting up logging, and performing specific cleaning tasks on various columns. The steps are:
<details>
    
- create class and initialize.
```sh
class DataCleaner:
    def __init__(self, dataframe):
        self.df = dataframe
        self.logger = setup_logger()
```

- convert dictionary column into the simple columns.
    ```sh
    def convert_dict_column(self, column_name):
        try:
            self.logger.info(f"Converting column '{column_name}' from text to dictionary.")
            expanded_df = self.df[column_name].apply(pd.Series)
            self.df = pd.concat([self.df.drop(columns=column_name), expanded_df], axis=1)
            self.logger.info(f"Column '{column_name}' successfully converted and expanded.")
        except Exception as e:
            self.logger.error(f"Error converting column '{column_name}': {e}")
    ```
    
- clean the rating column.
  
  ```sh
    def clean_ratings(self):
        def ratings(rating):
            try:
                dining_ratings = rating[0]
                dining_votes = rating[1]
                delivery_ratings = rating[3]
                delivery_votes = rating[4]
                return {
                    "dining_ratings": dining_ratings,
                    "dining_votes": dining_votes,
                    "delivery_ratings": delivery_ratings,
                    "delivery_votes": delivery_votes
                }
            except IndexError as e:
                self.logger.error(f"Error processing rating data: {e}")
                return {
                    "dining_ratings": None,
                    "dining_votes": None,
                    "delivery_ratings": None,
                    "delivery_votes": None
                }
        
        try:
            self.logger.info("Cleaning 'rating' column.")
            self.df['rating'] = self.df['rating'].apply(ratings)
            df_ratings = self.df['rating'].apply(pd.Series)
            self.df = pd.concat([self.df.drop(columns='rating'), df_ratings], axis=1)
            self.logger.info("'rating' column cleaned and expanded.")
        except Exception as e:
            self.logger.error(f"Error cleaning 'rating' column: {e}")
    ```

- clean the time column.
  
    ```sh
    def process_time_column(self):
        try:
            self.logger.info("Processing 'time' column.")
            self.df['days'] = self.df['time'].apply(lambda x: x.replace('Opening Hours\n','').split(':')[0])
            self.df['opening and closing time'] = self.df['time'].apply(lambda x: ":".join(x.replace('Opening Hours\n','').split(':')[1:]))
            self.df.drop(columns = 'time', inplace = True)
            self.logger.info("'time' column processed.")
        except Exception as e:
            self.logger.error(f"Error processing 'time' column: {e}")
    ```

</details>

## Overview of data cleaning of Swiggy

<details>

- **Create and Intitiate swiggyCleaner Class:** this step involved creating swiggy cleaner class and initiate it. 
```sh
class swiggyCleaner:
    def __init__(self, dataframe):
        self.df = dataframe
        self.logger = setup_logger()
```
- **Convert_restaurant_data:** In this step I have defined one function which will convert dictionary column into plain column.
  
```sh
    def convert_restaurant_data(self, column_name):
        f"""
        Normalize and expand the '{column_name}' column.
        """
        try:
            self.logger.info(f"Converting '{column_name}' column.")
            new_df = pd.json_normalize(self.df[column_name])
            self.df = pd.concat([self.df.drop(columns=f'{column_name}'), new_df], axis=1)
            self.logger.info(f"'{column_name}' column successfully converted.")
        except Exception as e:
            self.logger.error(f"Error converting '{column_name}' column: {e}")
```
- **Clean Ratings:** In this step I have defined one function which will clean the ratings column.
  
```sh

    def clean_ratings(self, text):
        """
        Extract ratings and number of reviews from a text string.
        """
        rating_match = re.search(r"(\d+\.\d+)", text)
        rating = rating_match.group(1) if rating_match else "Not specified"
        
        reviews_match = re.search(r"\(([\dKk\+]+) ratings?\)", text)
        reviews = reviews_match.group(1) if reviews_match else "Not specified"
        
        return {"rating": rating, "reviews": reviews}
```
- **Clean Category:** In this step I have defined one function which will clean the category column.

```sh

    def clean_category(self, element_list):
        """
        Clean elements in a list by removing unnecessary characters like commas and whitespace.
        """
        return [element.strip().rstrip(',') for element in element_list]

```
- **Clean Offer:** In this step I have defined one function which will clean the offer column.
  
```sh
    def clean_offer(self, offer_list):
        """
        Convert a list of offers into a dictionary.
        """
        offer_list = offer_list[1:]
        offers = {}
        for i in range(0, len(offer_list)):
            if i%2 ==0:
                offers[f'{offer_list[i]}'] = f'{offer_list[i+1]}'
        return offers
```
- **dish info:** In this step I have defined one function which will clean the dishes info. 
```sh

    def dish_info(self, paragraph):
        """
        Extract dish information from a paragraph.
        """
        data_list = paragraph.split('. ')
        veg_status = data_list[0] if len(data_list) > 0 else None
        dish_name = data_list[1] if len(data_list) > 1 else None
        items = paragraph.split(', ', 1)
        data_dict = {}

        for item in items:
            # Check if ': ' is in item before attempting to split
            if ': ' in item:
                key, value = item.split(': ', 1)
                data_dict[key.strip()] = value.strip()
            else:
                # If the item doesn't contain ': ', store the entire item with a None value
                data_dict[item.strip()] = None
        
        data_dict['veg_status'] = veg_status
        data_dict['dish_name'] = dish_name
        return data_dict
```
- **clean Reviews and Ratings:** In this step I have defined a function which will clean the reviews and ratings for the perticular restaurant.
```sh

    def clean_rating_reviews(self, text):
        """
        Clean and extract ratings and reviews from text.
        """
        text = text.replace('\n', ' ').replace('(', '').replace(')', '')
        parts = text.split()

        if len(parts) == 2:
            return {"rating": parts[0], "reviews": parts[1]}
        else:
            return {"rating": None, "reviews": None}
```
- **Dish Card Clean:** In this step I have defined a function which will take the help of dish info to clean all the dishes info using a for loop.
```sh

    def dish_card_clean(self, dish_data):
        """
        Clean and extract dish card information from a list of dishes.
        """
        data = []
        for dish in dish_data:
            info = self.dish_info(dish['dish_content'])
            rating = self.clean_rating_reviews(dish['ratings_content'])
            new = info | rating
            data.append(new)
        return data

```
- **Apply Transformation:** This is the final function which will used all the cleaning function to clean the dataset.
```sh
    def apply_transformations(self):
        """
        Apply all cleaning transformations to the dataframe and log the process.
        """
        try:
            self.logger.info("Starting data cleaning process.")

            # Convert 'restaurant_data' column
            self.convert_restaurant_data('restaurant_data')
            # Apply cleaning transformations to respective columns
            self.df['ratings'] = self.df['ratings'].apply(self.clean_ratings)
            self.logger.info('Raitngs Column cleaning process completed successfully')
            self.convert_restaurant_data('ratings')
            self.df['categories'] = self.df['categories'].apply(self.clean_category)
            self.logger.info('Category Column cleaning process completed successfully')
            self.df['offers'] = self.df['offers'].apply(self.clean_offer)
            self.logger.info('offers Column cleaning process completed successfully')
            self.df['dish_data'] = self.df['dish_data'].apply(self.dish_card_clean)
            self.logger.info('dish_data Column cleaning process completed successfully')

            self.logger.info("Data cleaning process completed successfully.")
        except Exception as e:
            self.logger.error(f"Error during data cleaning process: {e}")
```
- **Get Cleaned Dataframe:** this function will return the cleaned dataframe.
```sh

    def get_cleaned_dataframe(self):
        """
        Return the cleaned dataframe.
        """
        return self.df

```

</details>

## Overview Of zomatoMain.py
The main.py file orchestrates the process of scraping and cleaning Zomato restaurant data. It does the following:
<details>
    
- **Argument Parsing:** Reads command-line arguments for the Zomato URL and the number of restaurants to scrape.
```sh
def parse_arguments():
    parser = argparse.ArgumentParser(description='Scrape Zomato restaurant data.')
    parser.add_argument('--url', type=str, required=True, help='URL of the Zomato restaurant listing')
    parser.add_argument('--num', type=int, required=True, help='Number of restaurants to fetch')
    return parser.parse_args()
```
- **Data Scraping:** Fetches restaurant URLs and detailed data, saving the results to CSV files.
```sh
def scrape_data(url, num):
    scraper = RestaurantScraper(headless=False)
    restaurant_urls = scraper.get_restaurant_urls(url, num)
    
    df = pd.DataFrame(restaurant_urls, columns=['Web_link'])
    df.to_csv('web_links.csv', index=False)

    df['restaurant_data'] = df['Web_link'].apply(scraper.get_restaurant_data)
    df.to_csv('restaurant_data_uncleaned.csv', index=False)
    
    return df
```
- **Data Cleaning:** Processes and cleans the scraped data by transforming columns and standardizing values, then saves the cleaned data to a final CSV file.
```sh
def clean_data(df):
    cleaner = DataCleaner(df)
    cleaner.convert_dict_column('restaurant_data')
    cleaner.clean_ratings()
    cleaner.process_time_column()
    
    cleaned_df = cleaner.get_cleaned_dataframe()
    cleaned_df.to_csv('cleaned_restaurant_data.csv', index=False)
    
    return cleaned_df
```
</details>

</details>

## Streamlit App
The Streamlit app is designed to facilitate the scraping and cleaning of Zomato and swiggy restaurant data through a user-friendly web interface. 

<details>

```sh
import streamlit as st

# Set up the page configuration
st.set_page_config(page_title="Restaurant Scraper", layout="wide")



# App Description
st.write("""
## Welcome to the Restaurant Scraper App!

This app allows you to scrape restaurant data from two popular platforms: **Zomato** and **Swiggy**. 
Depending on your selection, the app will guide you through different steps for scraping.

### Zomato Scraping Instructions:
1. Provide the URL for the Zomato restaurant listings specific to a location for delivery.
2. Specify the number of restaurants to scrape.
3. Click the 'Start Scraping' button to begin the process.

### Swiggy Scraping Instructions:
1. Enter the location you want to scrape.
2. Click the 'Fetch Location' button to retrieve matching locations.
3. Select the desired location from the dropdown menu.
4. Specify the number of restaurants to scrape.
5. Click the 'Start Scraping' button to begin the process.
""")
```

</details>

![image](https://github.com/user-attachments/assets/ab2e3e4b-0e4d-46e3-a7f8-b3eb35b11c49)

## Zomato Scraper Page

<details>

```sh
import streamlit as st
import pandas as pd
from zomatoScraper import RestaurantScraper
from zomatoCleaner import DataCleaner
import time

# Function to scrape data
def scrape_data(url, num, progress_bar, status_message):
    # Step 1: Scrape restaurant URLs
    status_message.write('Restaurant links scraping, please wait...')
    scraper = RestaurantScraper(headless=True)
    restaurant_urls = scraper.get_restaurant_urls(url, num)
    
    df = pd.DataFrame(restaurant_urls, columns=['Web_link'])
    df.to_csv('web_links.csv', index=False)
    
    # Update progress to 33% after link scraping
    progress_bar.progress(33)
    
    # Step 2: Fetch restaurant data
    status_message.write('Restaurant data scraping, please wait...')
    df['restaurant_data'] = None
    
    for i, link in enumerate(df['Web_link']):
        df.at[i, 'restaurant_data'] = scraper.get_restaurant_data(link)
        progress_bar.progress(33 + int(33 * (i + 1) / len(df)))  # Incrementally update progress
    
    df.to_csv('uncleaned_restaurant_data.csv', index=False)
    return df

# Function to clean data
def clean_data(df, progress_bar, status_message):
    # Initialize DataCleaner with the DataFrame
    cleaner = DataCleaner(df)
    status_message.write('Data cleaning, please wait...')
    
    # Perform data cleaning
    cleaner.convert_dict_column('restaurant_data')
    progress_bar.progress(70)
    
    cleaner.clean_ratings()
    progress_bar.progress(85)
    
    cleaner.process_time_column()
    progress_bar.progress(95)
    
    # Get the cleaned DataFrame
    cleaned_df = cleaner.get_cleaned_dataframe()
    cleaned_df.to_csv('cleaned_restaurant_data.csv', index=False)
    progress_bar.progress(100)
    
    return cleaned_df

st.set_page_config(page_title="Zomato Scraper", page_icon="")
# def app():
# Streamlit app interface
st.title('Zomato Restaurant Scraper')
st.markdown('Enter the URL and number of restaurants to scrape.')

url = st.text_input('Restaurant Listing URL', 'https://www.zomato.com/ncr/delivery-in-connaught-place')
num = st.number_input('Number of Restaurants', min_value=1, value=25)

# Initialize or clear session state
if 'result_df' not in st.session_state:
    st.session_state.result_df = None

# Button to start scraping
if st.button('Start Scraping'):

    # Create message 
    status_message = st.empty()
    # Create single progress bar 
    progress_bar = st.progress(0)

    
    # Scrape data
    data_df = scrape_data(url, num, progress_bar, status_message)
    
    # Clean data
    result_df = clean_data(data_df, progress_bar, status_message)
    
    # Store the result in session state
    st.session_state.result_df = result_df
    
    status_message.write('Data is ready to download!')

# Display the results if available
if st.session_state.result_df is not None:
    st.dataframe(st.session_state.result_df)
    st.download_button('Download Restaurant Data CSV', st.session_state.result_df.to_csv(index=False), 'restaurant_data.csv', 'text/csv')

```
</details>

![image](https://github.com/user-attachments/assets/59fbf9d9-7829-4b23-9fbb-5985d0fc85b7)

## Swiggy Scraper Page

<details>

```sh

import streamlit as st
import pandas as pd
from swiggyScraper import swiggyScraper
from swiggyCleaner import swiggyCleaner


# Function to scrape restaurant URLs
def scrape_restaurant_urls(scraper, num, progress_bar, status_message):
    status_message.write('Scraping restaurant URLs, please wait...')
    restaurant_urls = scraper.get_restaurant_urls(num)
    
    df = pd.DataFrame(restaurant_urls, columns=['url'])
    df.to_csv('swiggy_restaurant_url.csv', index=False)
    
    # Update progress to 33%
    progress_bar.progress(33)
    return df

# Function to scrape restaurant data
def scrape_restaurant_data(df, scraper, progress_bar, status_message):
    status_message.write('Scraping restaurant data, please wait...')
    df['restaurant_data'] = None
    
    for i, url in enumerate(df['url']):
        df.at[i, 'restaurant_data'] = scraper.get_restaurant_data(url)
        progress_bar.progress(33 + int(33 * (i + 1) / len(df)))  # Incrementally update progress
    
    df.to_csv('swiggy_uncleaned_restaurant_data.csv', index=False)
    return df

# Function to clean data
def clean_data(df, progress_bar, status_message):
    status_message.write('Cleaning data, please wait...')
    cleaner = swiggyCleaner(df)
    
    # Perform data cleaning
    cleaner.apply_transformations()
    
    # Update progress bar incrementally during cleaning process
    progress_bar.progress(70)
    cleaned_df = cleaner.get_cleaned_dataframe()
    cleaned_df.to_csv('swiggy_cleaned_restaurant_data.csv', index=False)
    
    progress_bar.progress(100)
    return cleaned_df

st.set_page_config(page_title="Swiggy Scraper", page_icon="")
# def app():

# Initialize session state variables if they don't exist
if 'result_df' not in st.session_state:
    st.session_state['result_df'] = None
if 'fetch_location_done' not in st.session_state:
    st.session_state['fetch_location_done'] = False
if 'location_selected' not in st.session_state:
    st.session_state['location_selected'] = False
if 'option' not in st.session_state:
    st.session_state['option'] = None
if 'scraper' not in st.session_state:
    st.session_state['scraper'] = swiggyScraper()
# Streamlit app interface
st.title('Swiggy Restaurant Scraper')
st.markdown('Enter the location you want to scrape.')

location = st.text_input('Restaurant location', 'Connaught place')

# Button to fetch location
if st.button('Fetch location'):
    st.write('Fetching location...')
    scraper = st.session_state['scraper']
    location_dict = scraper.get_location(location)
    st.session_state['location_dict'] = location_dict  # Store in session state
    st.session_state['option'] = None  # Reset the option when a new location is fetched
    st.write("Locations fetched successfully.")
    st.session_state['fetch_location_done'] = True  # Indicate that location fetching is done

# Ensure 'location_dict' exists in session state
if 'location_dict' in st.session_state:
    location_dict = st.session_state['location_dict']
    location_list = list(location_dict.keys())  # Convert dict_keys to a list

    # Dropdown to select location
    option = st.selectbox(
        "Select one of the locations",
        [''] + location_list,  # Add an empty string as the first option
        index=0 if st.session_state.get('option') is None else location_list.index(st.session_state['option']),
        key='location_select',
    )

    # Button to confirm location selection
    if st.button('Confirm Location') and option and option != '':
        st.session_state['option'] = option  # Store the selected option in session state
        scraper = st.session_state['scraper']
        scraper.select_location(location_dict, option)
        st.session_state['location_selected'] = True  # Indicate location selection done

num = st.number_input('Number of Restaurants', min_value=1, value=25)

# Create message and progress bar
status_message = st.empty()
progress_bar = st.progress(0)

# Button to scrape data
if st.button('Start Scraping'):
    # Ensure that the fetch location and location selection are completed
    if not st.session_state.get('fetch_location_done'):
        st.write("Please fetch the location first.")
    elif not st.session_state.get('location_selected'):
        st.write("Please select a location first.")
    else:
        st.write('Starting to scrape...')
        scraper = st.session_state['scraper']
        
        # Step 1: Scrape URLs
        url_df = scrape_restaurant_urls(scraper, num, progress_bar, status_message)
        
        # Step 2: Scrape restaurant data
        data_df = scrape_restaurant_data(url_df, scraper, progress_bar, status_message)
        
        # Step 3: Clean the data
        result_df = clean_data(data_df, progress_bar, status_message)
        
        # Store the result in session state
        st.session_state.result_df = result_df
        
        status_message.write('Data is ready to download!')

# Display the results if available
if st.session_state.result_df is not None:
    st.dataframe(st.session_state.result_df)
    st.download_button('Download Restaurant Data CSV', st.session_state.result_df.to_csv(index=False), 'restaurant_cleaned_data.csv', 'text/csv')

```

</details>

![image](https://github.com/user-attachments/assets/1ac9546c-3962-4a99-8870-e5084497092d)

