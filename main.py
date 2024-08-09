from zomatoScraper import  RestaurantScraper

if __name__ == "__main__":
    try:
        # Create an instance of RestaurantScraper with headless mode enabled
        scraper = RestaurantScraper(headless=True)
        
        # Define the URL to scrape and the number of restaurant URLs to fetch
        link = 'https://www.zomato.com/ncr/delivery-in-connaught-place'  # Replace with your actual URL
        num = 10  # Number of URLs to fetch
        
        # Get restaurant URLs
        restaurant_urls = scraper.get_restaurant_urls(link, num)
        print(restaurant_urls)
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        
    finally:
        # Ensure WebDriver is closed
        scraper.close_driver()
