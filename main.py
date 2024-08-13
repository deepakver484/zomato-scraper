from zomatoScraper import  RestaurantScraper
import pandas as pd
from cleaner import DataCleaner
import argparse

# funcition for parsing arguments
def parse_arguments():
    parser = argparse.ArgumentParser(description='Scrape Zomato restaurant data.')
    parser.add_argument('--url', type=str, required=True, help='URL of the Zomato restaurant listing')
    parser.add_argument('--num', type=int, required=True, help='Number of restaurants to fetch')
    return parser.parse_args()

# Function to scrape data
def scrape_data(url, num):
    scraper = RestaurantScraper(headless=True)
    restaurant_urls = scraper.get_restaurant_urls(url, num)
    
    df = pd.DataFrame(restaurant_urls, columns=['Web_link'])
    df.to_csv('web_links.csv', index=False)

    df['restaurant_data'] = df['Web_link'].apply(scraper.get_restaurant_data)
    df.to_csv('restaurant_data_uncleaned.csv', index=False)
    
    return df

# Function to clean data
def clean_data(df):
    cleaner = DataCleaner(df)
    cleaner.convert_dict_column('restaurant_data')
    cleaner.clean_ratings()
    cleaner.process_time_column()
    
    cleaned_df = cleaner.get_cleaned_dataframe()
    cleaned_df.to_csv('cleaned_restaurant_data.csv', index=False)
    
    return cleaned_df

if __name__ == "__main__":
    args = parse_arguments()

    # Scrape the data
    scraped_data = scrape_data(args.url, args.num)
    
    # Clean the data
    cleaned_data = clean_data(scraped_data)