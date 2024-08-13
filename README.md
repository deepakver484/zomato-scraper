# ZOMATO SCRAPER

## Objective -

The primary objective of this project is to develop an automated data pipeline that scrapes restaurant information from Zomato, processes and cleans the scraped data, and outputs it in a structured format. This pipeline is designed to be flexible, allowing users to specify the URL of the Zomato restaurant listing and the number of restaurants to scrape. The cleaned data is then stored in a CSV file, making it ready for further analysis or reporting.

## Website Selection - 

I chose to scrape Zomato due to its rich and diverse dataset that offers valuable insights into restaurants, food trends, and customer preferences. Zomato's dynamic HTML content, including elements that are loaded lazily, presents a unique challenge in data extraction. This complexity is particularly evident in dynamic elements like tooltips within SVG elements, which require advanced handling to ensure accurate data capture. Despite these challenges, the quality of data available on Zomato is excellent, making it a valuable source for detailed analysis and insights.

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
| [**main.py**](https://github.com/deepakver484/zomato-scraper/main.py)                           | Main pipeline script for executing tasks in shell mode.   |
| [**requirements.txt**](https://github.com/deepakver484/zomato-scraper/requirements.txt)         | Lists Python dependencies for the project.                |
| [**app.py**](https://github.com/deepakver484/zomato-scraper/app.py)                             | app.py file consist streamlit app code.                   |
| [**cleaner.py**](https://github.com/deepakver484/zomato-scraper/cleaner.py)                     | cleaner.py file consist cleaning code.                    |
| [**zomatoScraper.py**](https://github.com/deepakver484/zomato-scraper/zomatoScraper.py)         | file consist all the scraping code for zomato.            |
| [**web_links.csv**](https://github.com/deepakver484/zomato-scraper/web_links.csv)                   | csv file consist data of restaurant's url.                   |
| [**restaurant_data_uncleaned.csv**](https://github.com/deepakver484/zomato-scraper/restaurant_data_uncleaned.csv)                   | csv file consist restaurant's uncleaned data. |
| [**cleaned_restaurant_data.csv**](https://github.com/deepakver484/zomato-scraper/cleaned_restaurant_data.csv)                   | csv file consist restaurant's cleaned data.       |
| [**utils.py**](https://github.com/deepakver484/zomato-scraper/utils.py)                   | file consist common base functions.       |





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

## Run Pipeline

 To run pipeline in background run below given python command
```sh
python main.py --url "https://www.zomato.com/ncr/delivery-in-connaught-place" --num 1
```
**url** - you can use any url from the zomato website for online delivery.

**num** - number of restaurants you want to scrap.

## Run Strealit App
7. To run streamlit app
```sh
streamlit run app.py
```

## Detailed approach for the Project
1. first step involves data scraping from the zomato
I break down this problem into two major parts first scrap the links of restaurant from the main page
then scrap data of each restaurants
further break down restaurants data scraping into the below given parts
first scrap the data of the head element
include name, address, categories, operational days, opening and closing time, latitude and longitude, delivery ratings and Dining ratings,
next step involved 
get the order section 
then get all the dish card from the order section
in next step we iterate through each dish card to get the below given data
name, rating,price, veg type and description
<details>
  
## Scraping Code Setup

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

  
- Configure the screenshot capture function.
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

## Data Scraping from Zomato: The first step involves scraping data from Zomato. This process is divided into two main parts:
<details>
 
**Scraping Restaurant Links:** Initially, we extract the links to individual restaurants from the main page.
```sh
    def get_restaurant_urls(self, link, num):
        try:
            self.logger.info(f"Fetching restaurant URLs from {link}")
            self.driver.get(link)
            sleep(5)

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
```
- **Scraping Restaurant Data:** Once we have the restaurant links, we proceed to scrape detailed data for each restaurant. This process is further divided into several sub-tasks:
  ```sh
    def get_restaurant_data(self, restaurant_link):
        try:
            self.logger.info(f"Fetching restaurant data from URL {restaurant_link}")

            # getting the restaurant link
            self.driver.get(restaurant_link)
            sleep(5)
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
        head_div = self.try_element('xpath', '//div[contains(text(),"Ratings")]/../../../../..')
        
        # finding name of the restaurant
        name_element = self.try_element('TAG_NAME', 'h1', driver= head_div)
        name = name_element.text
        
        # finding the resaurants ratings
        rating_element = self.try_element('XPATH', '//div[contains(text(),"Ratings")]/../../..')
        rating = rating_element.text.split('\n')
        
        # finding the categories restaurant served
        category_element = self.try_element('XPATH', '//div[contains(text(),"Ratings")]/../../../../../../section[1]/div')
        category = category_element.text.split(', ')
        
        #finding the location of the restaurant
        location_element = self.try_element('XPATH','//div[contains(text(),"Ratings")]/../../../../../../section[1]/a')
        location = location_element.text.split(', ')
        
        # finding the opening and closing time
        tooltip_xpath = '//div[@role ="tooltip"]'
        text_element = '//span[@role="tooltip"]'
        time = self.get_dynamic_tooltip_text(tooltip_xpath=tooltip_xpath, text_element=text_element)
        
        #findnig the cordinates of the restaurant
        destination_element = self.try_element('XPATH', '//span[contains(text(),"Direction")]/../..')
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
        tooltip_element = self.try_element('xpath', tooltip_xpath)

        action = ActionChains(self.driver)
        #moving cursor to hover over the tooltip div to activate the script
        action.move_to_element(tooltip_element).perform()
            
        # Capture the tooltip's text from the displayed elements
        tooltip_text = self.try_element('xpath', text_element).text
        return tooltip_text
    ```

  - **Order Section:** Next, we scrape the order section of the restaurant page.
  ```sh
    def extract_order_sections(self):

        # Find the order sections after the first one
        order_section = self.try_element('xpath', '//h2[contains(text(),"Order Online")]/../../../section', element=False)
        order_section = order_section[1:]  # Skip the first section due not having the relevent content
        
        order_div = []
        # Loop through each section and find div elements with text
        for sec in order_section:
            divs = self.try_element('xpath', 'div', driver = sec, element=False)
            self.logger.info(f"Found {len(divs)} div elements in section.")
            for div in divs:
                if div.text:
                    order_div.append(div)
                    self.logger.debug(f"Appended div with text: {div.text}")

        dish_card = []
        # Loop through each order div and find inner div elements
        for div in order_div:
            dish_card += self.try_element('xpath', 'div', driver = div, element=False)
            self.logger.info(f"Extracted {len(dish_card)} dish cards so far.")

        return dish_card
  ```

  - **Dish Cards:** We then extract all the dish cards from the order section. For each dish card, we gather detailed information including the dish name, rating, price, vegetarian type, and description.
    ```sh
    def extract_dish_card(self, dish_card):
        # Extract the dish name
        dish_name = self.try_element('tag_name', 'H4', driver=dish_card).text
            
        # Extract the number of votes
        dish_votes = self.try_element('xpath', './/span[contains(text(), "votes")]', driver = dish_card).text
            
        # Extract the dish price
        dish_price = self.try_element('xpath', './/span[contains(text(), "₹")]', driver = dish_card).text

        # Check if the "read more" button for description exists and click it if found
        dish_description_read_more = self.try_element('xpath', './/span[contains(text(), "read more")]', driver = dish_card)
        if dish_description_read_more.text != 'Not found':
            dish_description_read_more.click()
            self.logger.info("Clicked on 'read more' for dish description.")

        # Extract the dish description
        dish_description = self.try_element('tag_name', 'p', driver = dish_card).text

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

  - **Ratings & veg type of the Dish:** this will get the ratings from the dish card
```sh
    def ratings_dish_card(self, dish_card):
        counter = 0
        i_tags = self.try_element('tag_name', 'i', element=False, driver = dish_card)
        
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
            i_element = self.try_element('tag_name', 'title', driver = i_tag)
            if i_element.text != 'Not found':
                # increase the counter rating
                counter += 1
            else:
                # getting the decimal of the rating
                last = self.try_element('xpath', './/*[local-name()="stop" and @stop-color="#F3C117"]', element=False,driver= i_tag)
                if len(last) == 0:
                    break
                else:
                    last = last[1]
                counter += int(last.get_attribute('offset').replace('%', '')) * 0.01
                break
        return counter, dish_type
```
</details> 
</details>

## Detailed approach for the data cleaning
This section outlines a comprehensive approach for data cleaning. The process includes initializing a class, setting up logging, and performing specific cleaning tasks on various columns. The steps are:
<details>
    
- create class and initialize.
```sh
class DataCleaner:
    def __init__(self, dataframe):
        self.df = dataframe
        self.logger = self._setup_logger()
```

- create logger function.
```sh
    def _setup_logger(self):
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(handler)
        return logger
```

- convert dictionary column into the simple columns.
  ```sh
    def convert_dict_column(self, column_name):
        try:
            self.logger.info(f"Converting column '{column_name}' from text to dictionary.")
            # self.df[column_name] = self.df[column_name].apply(ast.literal_eval)
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
- clean the timem column.
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

## Overview Of Main.py
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
    scraper = RestaurantScraper(headless=True)
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

## Streamlit App 
![image](https://github.com/user-attachments/assets/f13d6b34-f178-41b6-975a-e4c804c1e3e7)

## Overview of Streamlit App
The Streamlit app is designed to facilitate the scraping and cleaning of Zomato restaurant data through a user-friendly web interface. It allows users to input a URL and the number of restaurants to scrape, then performs the following steps:
<details>

- **Data Scraping:** Collects restaurant URLs and detailed information, updating progress and status messages to keep the user informed.
    
  ```sh
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
    
    df.to_csv('restaurant_data.csv', index=False)
    return df
  ```
- **Data Cleaning:** Processes the scraped data to improve its quality, updating the progress bar as each cleaning step is completed.
  ```sh
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
  ```
- **User Interaction:** Provides a button to start the scraping and cleaning process, displays the resulting data in a table, and offers a download option for the cleaned data.
  ```sh
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
The app uses progress bars and status messages to give real-time feedback on the progress of data processing and allows users to download the cleaned data in CSV format.
</details>


