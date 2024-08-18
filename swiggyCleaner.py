import pandas as pd
import re
from utils import setup_logger

class swiggyCleaner:
    def __init__(self, dataframe):
        self.df = dataframe
        self.logger = setup_logger()

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


    def clean_ratings(self, text):
        """
        Extract ratings and number of reviews from a text string.
        """
        rating_match = re.search(r"(\d+\.\d+)", text)
        rating = rating_match.group(1) if rating_match else "Not specified"
        
        reviews_match = re.search(r"\(([\dKk\+]+) ratings?\)", text)
        reviews = reviews_match.group(1) if reviews_match else "Not specified"
        
        return {"rating": rating, "reviews": reviews}


    def clean_category(self, element_list):
        """
        Clean elements in a list by removing unnecessary characters like commas and whitespace.
        """
        return [element.strip().rstrip(',') for element in element_list]


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


    def get_cleaned_dataframe(self):
        """
        Return the cleaned dataframe.
        """
        return self.df


