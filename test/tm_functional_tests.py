import unittest
from tm_web_scraper import TransfermarktScraper
import sys

class KickerFunctionalTest(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, "../src")
        self.browser = TransfermarktScraper()
        self.url_md = "https://www.transfermarkt.com/"
    
    def tearDown(self) -> None:
        self.browser.tear_down()
    
    def test_get_page(self):
        driver = self.browser.get_driver()
        driver.get("http://www.google.com")

        self.assertIn("Google", driver.title)

        #self.fail("Finish the test!")

    def test_load_page(self):
        self.assertTrue(self.browser.load_page(self.url_md))   

        title = self.browser.get_driver().title
        self.assertIn("Bundesliga heute", title, "The title does not contain 'Bundesliga heute'")


class TransfermarktUnitTest(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, "../src")
        self.browser = TransfermarktScraper()
        self.url_pi = "https://www.kicker.de/matthijs-de-ligt/spieler/bundesliga/2023-24/fc-bayern-muenchen"
        self.url_pii = "https://www.kicker.de/jordan-siebatcheu/spieler/bundesliga/2023-24/bor-moenchengladbach" 
        self.urls = [self.url_pi, self.url_pii, "https://www.kicker.de/jordan-siebatcheu/spieler/bundesliga/2023-24/bor-moenchengladbach"]

        self.test_cases = [
            {
                "url": "https://www.kicker.de/matthijs-de-ligt/spieler/bundesliga/2023-24/fc-bayern-muenchen",
                "expected": {"name": "Jordan Siebatcheu", "club": "Bor. Mönchengladbach", "season": "2023-24"}
            },
            {
                "url": "https://www.kicker.de/jordan-siebatcheu/spieler/bundesliga/2023-24/bor-moenchengladbach",
                "expected": {"name": "Another Player", "club": "Another Club", "season": "2023-24"}
            },
            {   "url": "https://www.kicker.de/patrick-herrmann-2/spieler/bundesliga/2023-24/bor-moenchengladbach",
                "expected": {"name": "Another Player", "club": "Another Club", "season": "2023-24"}
            },
        ]


        self.url_mi = "https://www.kicker.de/bremen-gegen-bayern-2023-bundesliga-4861795/spielinfo"
        self.url_me = "https://www.kicker.de/wolfsburg-gegen-heidenheim-2023-bundesliga-4861971/schema"
        self.url_mg = "https://www.kicker.de/augsburg-gegen-mgladbach-2023-bundesliga-4861973/schema"
        #self.url_mg = "https://www.kicker.de/dortmund-gegen-koeln-2023-bundesliga-4861967/schema"

        self.url_md = "https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1/plus/?saison_id=2023"
        self.url_club = "https://www.transfermarkt.com/bayern-munich/kader/verein/27/saison_id/2024/plus/1"

    def tearDown(self) -> None:
        self.browser.tear_down()

    def test_get_clubs_info(self):
        # https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1/plus/?saison_id=2023
        clubs_info = self.browser.get_teams_info_per_competition_and_season(self.url_md)
        self.assertIsInstance(clubs_info, list)
        self.assertTrue(all(isinstance(link, dict) for link in clubs_info)) # list of dicts with club name and url
        self.assertTrue(len(clubs_info) == 18)

    def test_get_club_portrait(self):
        # https://www.transfermarkt.com/fc-bayern-munchen/datenfakten/verein/27
        # https://www.transfermarkt.com/fc-bayern-munchen/stadion/verein/27/saison_id/2024
        clubs_info = self.browser.get_club_portrait("https://www.transfermarkt.com/fc-bayern-munchen/datenfakten/verein/27")
        self.assertIsInstance(clubs_info, list)
        self.assertTrue(all(isinstance(link, dict) for link in clubs_info)) # list of dicts with club name and url
        self.assertTrue(len(clubs_info) == 18)

    def test_get_stadium_overview(self):
        # https://www.transfermarkt.com/fc-bayern-munchen/datenfakten/verein/27
        clubs_info = self.browser.get_stadium_overview("https://www.transfermarkt.com/fc-bayern-munchen/stadion/verein/27/saison_id/2024")
        self.assertIsInstance(clubs_info, list)
        self.assertTrue(all(isinstance(link, dict) for link in clubs_info)) # list of dicts with club name and url
        self.assertTrue(len(clubs_info) == 18)

    def test_get_all_players_from_team(self):
        # https://www.transfermarkt.com/bayern-munich/kader/verein/27/saison_id/2024/plus/1
        clubs_urls = self.browser.get_all_players_from_team(self.url_club)

        self.assertIsInstance(clubs_urls, list)
        self.assertTrue(all(isinstance(link, str) for link in clubs_urls)) # list of urls of a club's players
        self.assertTrue(len(clubs_urls) == 28)

    def test_get_player_profile(self):
        self.browser = TransfermarktScraper()

        player_profile = self.browser.get_player_profile_from_team("https://www.transfermarkt.com/alphonso-davies/profil/spieler/424204")

        self.assertIsInstance(player_profile, dict) # dict of player's attributes like name, birthdate, ...
        self.assertTrue("last_name" in player_profile)
        self.assertTrue("Position:" in player_profile)
        
        #self.assertEqual("Matthijs de Ligt", player["name"])
        #self.assertEqual(188, player["height"])

    def test_get_player_stats(self):
        self.browser = TransfermarktScraper()

        player_stats = self.browser.get_player_stats_from_team("https://www.transfermarkt.com/jamal-musiala/leistungsdaten/spieler/580195/saison/2023/plus/1#gesamt")

        self.assertIsInstance(player_stats, dict) # dict of a player stats
        self.assertTrue(len(player_stats) == 14)
        self.assertEqual("Competiton" in player_stats)
        self.assertEqual("Minutes per goal" in player_stats)
        #self.assertEqual(188, player["height"])

    def test_get_market_values(self):
        self.browser = TransfermarktScraper()

        market_values = self.browser.get_market_values("https://www.transfermarkt.com/jamal-musiala/profil/spieler/580195")

        self.assertIsInstance(market_values, dict)
        self.assertTrue(len(market_values) == 10)
        #self.assertEqual("Matthijs de Ligt", player["name"])
        #self.assertEqual(188, player["height"])

    def test_get_matchday_details(self):
        self.browser = TransfermarktScraper()

        md_details = self.browser.get_matchday_details("https://www.transfermarkt.com/bundesliga/spieltag/wettbewerb/L1/saison_id/2023/spieltag/1")

        self.assertIsInstance(md_details, dict)
        self.assertTrue(len(md_details) == 10)
        #self.assertEqual("Matthijs de Ligt", player["name"])
        #self.assertEqual(188, player["height"])

    def test_get_match_details(self):
        self.browser = TransfermarktScraper()

        match_details = self.browser.get_match_details("https://www.transfermarkt.com/spielbericht/index/spielbericht/4095967")

        self.assertIsInstance(match_details, dict)
        self.assertTrue(len(match_details) == 10)
        #self.assertEqual("Matthijs de Ligt", player["name"])
        #self.assertEqual(188, player["height"])

    def test_get_goal_details(self):
        self.browser = TransfermarktScraper()

        goal_details = self.browser.get_goals_details_per_match("https://www.transfermarkt.com/spielbericht/index/spielbericht/4095970")

        self.assertIsInstance(goal_details, dict)
        self.assertTrue(len(goal_details) == 10)
        #self.assertEqual("Matthijs de Ligt", player["name"])
        #self.assertEqual(188, player["height"])

    def test_get_top_players(self):
        self.browser = TransfermarktScraper()

        goal_details = self.browser.get_top_players_per_match("https://www.transfermarkt.com/spielbericht/index/spielbericht/4095970")

        self.assertIsInstance(goal_details, dict)
        self.assertTrue(len(goal_details) == 10)
        #self.assertEqual("Matthijs de Ligt", player["name"])
        #self.assertEqual(188, player["height"])

    def test_get_player_ratings(self):
        self.browser = TransfermarktScraper()

        goals = self.browser.get_player_ratings_per_match("https://www.transfermarkt.com/bayer-04-leverkusen_rb-leipzig/aufstellung/spielbericht/4095970")

        self.assertIsInstance(goals, list)
        self.assertTrue(len(goals) == 8)
        #self.assertEqual("Matthijs de Ligt", goals["name"])
        #self.assertEqual(188, goals["height"]))

if __name__ == "__main__":
    sys.path.insert(0, "../src")
    unittest.main()