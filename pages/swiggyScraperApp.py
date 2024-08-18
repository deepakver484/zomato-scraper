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
