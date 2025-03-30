import unittest
from manga_web_scraping.utils.scraper import search_and_select, extract_item_details

class TestScraper(unittest.TestCase):

    def test_search_and_select(self):
        # Test the search_and_select function with a mock URL
        search_url = "https://mto.to/search?word=test"
        item_url = search_and_select(search_url)
        self.assertIsInstance(item_url, str)
        self.assertTrue(item_url.startswith("http"))

    def test_extract_item_details(self):
        # Test the extract_item_details function with a mock item URL
        item_url = "https://mto.to/item/test-item"
        details = extract_item_details(item_url)
        self.assertIsInstance(details, dict)
        self.assertIn('title', details)
        self.assertIn('author', details)

if __name__ == '__main__':
    unittest.main()