import os

# Flipkart search URL
FLIPKART_URL = "https://www.flipkart.com/search?q=iphone+16"

# WebDriver path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHROME_DRIVER_PATH = os.path.join(BASE_DIR, "../drivers/chromedriver.exe")

# CSV Output File
CSV_FILE = os.path.join(BASE_DIR, "../data/iphone_prices.csv")
