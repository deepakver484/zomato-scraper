import streamlit as st
import pandas as pd
from zomatoScraper import RestaurantScraper
import time

# Function to scrape data
def scrape_data(url, num):
    st.write('Scraping data, please wait...')
    
    # First operation: Get restaurant URLs
    progress_bar1 = st.progress(0)
    scraper = RestaurantScraper(headless=True)
    restaurant_urls = scraper.get_restaurant_urls(url, num)
    
    df = pd.DataFrame(restaurant_urls, columns=['Web_link'])
    df.to_csv('web_links.csv', index=False)
    progress_bar1.progress(100)
    
    # Second operation: Fetch restaurant data
    progress_bar2 = st.progress(0)
    df['restaurant_data'] = None
    
    for i, link in enumerate(df['Web_link']):
        df.at[i, 'restaurant_data'] = scraper.get_restaurant_data(link)
        progress_bar2.progress((i + 1) / len(df))
        time.sleep(0.1)  # Simulate some delay for visualization purposes
    
    df.to_csv('restaurant_data.csv', index=False)
    return df

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
    result_df = scrape_data(url, num)
    st.session_state.result_df = result_df
    st.write('Data is ready to download!')

# Display the results if available
if st.session_state.result_df is not None:
    df = pd.read_csv('web_links.csv')
    st.dataframe(df)
    st.download_button('Download Restaurant Links CSV', st.session_state.result_df[['Web_link']].to_csv(index=False), 'web_links.csv', 'text/csv')
    st.dataframe(st.session_state.result_df)
    st.download_button('Download Restaurant Data CSV', st.session_state.result_df.to_csv(index=False), 'restaurant_data.csv', 'text/csv')

