import unittest
import json
from football_repository_controller import *

class FootballRepositoryControllerTestCases(unittest.TestCase):
    def setUp(self):
        self.frc = FootballRepositoryController() 
    
    def tearDown(self) -> None:
        pass

    def test_load_repository(self):
        self.frc._load_clubs_info()

    def test_crawl_and_save_clubs(self):
        self.frc.crawl_and_save_clubs("bundesliga", "2023")
        pass
    
    def test_scrape_and_save_club_details(self):
        clubs_portrait = self.frc.scrape_and_save_club_details("2023", "bundesliga")
        print(clubs_portrait)

    
