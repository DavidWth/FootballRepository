import unittest
from selenium import webdriver

class KickerTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
    
    def tearDown(self) -> None:
        self.browser.quit()
    
    def test_get_matchday(self):
        self.browser.get("http://www.google.com")

        self.assertIn("Google", self.browser.title)

        self.fail("Finish the test!")
    
if __name__ == "__main__":
    unittest.main()