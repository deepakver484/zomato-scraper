import logging
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# This class mimics a WebElement with a .text attribute set to "Not found". 
# This class can be returned when an element is not found.
class DummyElement:
    def __init__(self, text="Not found"):
        self.text = text

    def get_attribute(self, attribute):
        return "Not found"
    



# setting up logger function
def setup_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
    logger.addHandler(handler)
    return logger

def take_screenshot(driver, logger, filename):
    """Take a screenshot and save it to the specified file."""
    driver.save_screenshot(filename)
    logger.info(f"Screenshot saved as {filename}")


'''
    try_element function - this function handles the error (elements not found)
    params:-
    tay_type - it is the type of element I am searching on it
    tag_path - is is either class ,tagname or xpath
    element - bool (either finding (element :- True) or (elements :- False))
    '''
def try_element(tag_type, tag_path, driver, logger, element = True):
    result = None

    if element:
        try:
            by_type = getattr(By, tag_type.upper())
            result = driver.find_element(by_type, tag_path)
        except NoSuchElementException:
            result = DummyElement()
            logger.warning(f"Element not found with {tag_type}='{tag_path}'")

    else:
        try:
            by_type = getattr(By, tag_type.upper())
            result = driver.find_elements(by_type, tag_path)
        except NoSuchElementException:
            result = DummyElement()
            logger.warning(f"Elements not found with {tag_type}='{tag_path}'")

    return result