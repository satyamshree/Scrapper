import unittest
from src.scraper import scrape_flipkart

class TestScraper(unittest.TestCase):
    def test_scraper(self):
        """Check if scraping returns data."""
        scrape_flipkart()
        with open("data/iphone_prices.csv", "r") as f:
            self.assertTrue(len(f.readlines()) > 1)

if __name__ == "__main__":
    unittest.main()
