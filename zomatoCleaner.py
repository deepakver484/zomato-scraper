import pandas as pd
from utils import setup_logger


class DataCleaner:
    def __init__(self, dataframe):
        self.df = dataframe
        self.logger = setup_logger()

    '''
    converting dictionary column into plan columns
    params - column_name you want to convert into plain column
    '''  
    def convert_dict_column(self, column_name):
        try:
            self.logger.info(f"Converting column '{column_name}' from text to dictionary.")
            expanded_df = self.df[column_name].apply(pd.Series)
            self.df = pd.concat([self.df.drop(columns=column_name), expanded_df], axis=1)
            self.logger.info(f"Column '{column_name}' successfully converted and expanded.")
        except Exception as e:
            self.logger.error(f"Error converting column '{column_name}': {e}")
    '''
    this is for cleaning ratings column
    '''
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

    '''
    this is for cleaning time column
    '''
    def process_time_column(self):
        try:
            self.logger.info("Processing 'time' column.")
            self.df['days'] = self.df['time'].apply(lambda x: x.replace('Opening Hours\n','').split(':')[0])
            self.df['opening and closing time'] = self.df['time'].apply(lambda x: ":".join(x.replace('Opening Hours\n','').split(':')[1:]))
            self.df.drop(columns = 'time', inplace = True)
            self.logger.info("'time' column processed.")
        except Exception as e:
            self.logger.error(f"Error processing 'time' column: {e}")
    '''
    this function is for get the cleaned dataframe
    '''
    def get_cleaned_dataframe(self):
        return self.df