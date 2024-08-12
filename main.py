from zomatoScraper import  RestaurantScraper
import pandas as pd
import json


if __name__ == "__main__":
    # Create an instance of RestaurantScraper with headless mode enabled
    scraper = RestaurantScraper(headless=True)
        
    # Define the URL to scrape and the number of restaurant URLs to fetch
    link = 'https://www.zomato.com/ncr/delivery-in-connaught-place'  # Replace with your actual URL
    num = 25  # Number of Restaurants to fetch

    # Get restaurant URLs
    restaurant_urls = scraper.get_restaurant_urls(link, num)
    
    # saving restaurant URLs into the a csv name called web_links.csv
    df = pd.DataFrame(restaurant_urls, columns =['Web_link'])
    df.to_csv('web_links.csv', index=False)

    df['restaurant_data'] = df['Web_link'].apply(scraper.get_restaurant_data)

    df.to_csv('restaurant_data.csv', index= False)
