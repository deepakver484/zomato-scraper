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