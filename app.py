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
    
    df.to_csv('cleaned_restaurant_data.csv', index=False)
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
