import unittest
from web_scraper import KickerScraper
import sys
from import_export_json import save_to_json

class KickerFunctionalTest(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, "../src")
        self.browser = KickerScraper()
        self.url_md = "https://www.kicker.de/bundesliga/spieltag/2023-24/1"
        self.url_mi = "https://www.kicker.de/bremen-gegen-bayern-2023-bundesliga-4861795/spielinfo"
        self.url_me = "https://www.kicker.de/wolfsburg-gegen-heidenheim-2023-bundesliga-4861971/schema"
    
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

    def test_get_fixture_links(self):
        fixture_links = self.browser.get_fixture_links(self.url_md)
        self.assertIsInstance(fixture_links, list)
        self.assertTrue(all(isinstance(link, str) for link in fixture_links))
        self.assertTrue(len(fixture_links) == 9)

    def test_get_match_info(self):
        #self.browser.load_page(self.url_mi)
        match_info = self.browser.get_match_details(self.url_mi)
        self.assertIsInstance(match_info, dict)
        self.assertTrue(len(match_info) == 9)

    # def test_get_match_goals(self):
    #     self.browser.load_page(self.url_me)
    #     match_goals = self.browser.get_match_goals_info(self.url_me)
    #     #self.assertIsInstance(match_goals, dict)
    #     #self.assertTrue(len(match_goals) == 9)

    def test_get_club_controller(self):
        url_clubs = "https://www.kicker.de/bundesliga/teams/2023-24"
        self.browser = KickerScraper()

        clubs = self.browser.get_teams_info_per_competition_and_season(url_clubs)

        self.assertIsInstance(clubs, list)
        self.assertTrue(len(clubs) == 18)

    def test_get_all_players_from_team(self):
        url_team_players = "https://www.kicker.de/bor-moenchengladbach/kader/bundesliga/2023-24"
        self.browser = KickerScraper()

        players = self.browser.get_players_profile_from_team(url_team_players)

        self.assertIsInstance(players, list)
        self.assertTrue(len(players) == 27)
        
    def test_e2e(self):
        url_teams = "https://www.kicker.de/bundesliga/teams/2023-24"
        self.browser = KickerScraper()

        self.browser.get_all_per_season(url_teams)

#        self.assertIsInstance(players, list)
#       self.assertTrue(len(players) == 18)
    def test_load_fixtures_and_events_and_save_to_json(self):
        self.browser = KickerScraper()
        season_fixtures, goals = self.browser.load_all_fixtures_and_events(stop=3)

        save_to_json(season_fixtures, "season_fixtures.json")
        save_to_json(goals, "goals.json")

        self.assertTrue(len(season_fixtures) == 24)
        self.assertIsInstance(goals, list)

    def test_get_club_codes(self):
        self.browser = KickerScraper()
        club_codes = self.browser.get_club_codes()

        # check if club codes are been taking from cache now
        self.browser.get_club_codes()
        
        self.assertIsInstance(club_codes, dict)
        self.assertTrue(len(club_codes) == 18)
        

class KickerUnitTest(unittest.TestCase):
    def setUp(self):
        sys.path.insert(0, "../src")
        self.browser = KickerScraper()
        self.url_ti = "https://www.kicker.de/bayer-04-leverkusen/info/bundesliga/2023-24"
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

        self.url_md = "https://www.kicker.de/bundesliga/spieltag/2023-24/1"
        self.url_mi = "https://www.kicker.de/bremen-gegen-bayern-2023-bundesliga-4861795/spielinfo"
        self.url_me = "https://www.kicker.de/wolfsburg-gegen-heidenheim-2023-bundesliga-4861971/schema"
        self.url_mg = "https://www.kicker.de/augsburg-gegen-mgladbach-2023-bundesliga-4861973/schema"
        #self.url_mg = "https://www.kicker.de/dortmund-gegen-koeln-2023-bundesliga-4861967/schema"
    
    def tearDown(self) -> None:
        self.browser.tear_down()

    def test_get_stadium_info(self):
        self.browser = KickerScraper()
        url_stadium = "https://www.kicker.de/fc-bayern-muenchen/team-stadion/bundesliga/2024-25"

        stadium = self.browser.get_stadium_info(url_stadium)

        self.assertEqual("Allianz-Arena", stadium["name"])
        self.assertEqual(75024, stadium["totalCapacity"])

    def test_get_stadium_info_with_wrong_url(self):
        self.browser = KickerScraper()
        url_stadium = "https://www.kicker.de/afke-team/team-stadion/bundesliga/2024-25"

        stadium = self.browser.get_stadium_info(url_stadium)

        self.assertEqual("Allianz-Arena", stadium["name"])
        self.assertEqual(75024, stadium["totalCapacity"])

    def test_get_team(self):
        self.browser = KickerScraper()

        team = self.browser.get_team_profile(self.url_ti)

        self.assertIsInstance(team, dict)
        self.assertTrue(len(team) == 4)
        self.assertEqual("bayer-04-leverkusen", team["slug"])
        self.assertEqual("Bayer 04 Leverkusen", team["name"])
        self.assertEqual(62000, team["members"])

    def test_get_player_profile(self):
        self.browser = KickerScraper()

        #  for number in (2, 4, 6, 8, 10):
        #     with self.subTest(number=number):
        #         assert is_even(number)
        for case in self.test_cases:
            with self.subTest(url=case["url"]):
                player = self.browser.get_player_profile_from_team(case["url"])

                self.assertIsInstance(player, dict)
                self.assertTrue(len(player) == 10)
        #self.assertEqual("Matthijs de Ligt", player["name"])
        #self.assertEqual(188, player["height"])

    def test_get_match_goals_info(self):
        self.browser = KickerScraper()

        goals = self.browser.get_match_goals_info(self.url_mg)

        self.assertIsInstance(goals, list)
        self.assertTrue(len(goals) == 8)
        #self.assertEqual("Matthijs de Ligt", goals["name"])
        #self.assertEqual(188, goals["height"])

    def test_transform_goals(self):
        self.browser = KickerScraper()
        kicker_goals = [{0: '', 1: '', 2: '0\n:\n1', 3: "13'", 4: 'Itakura\nKopfball, Honorat'}, {0: '', 1: '', 2: '0\n:\n2', 3: "27'", 4: 'Cvancara\nRechtsschuss, Weigl'}, {0: 'Rexhbecaj\nLinksschuss, Michel', 1: "29'", 2: '1\n:\n2', 3: '', 4: ''}, {0: '', 1: '', 2: '1\n:\n3', 3: "37'", 4: 'Ngoumou\nRechtsschuss, Omlin'}, {0: 'M. Bauer\nRechtsschuss, Demirovic', 1: "41'", 2: '2\n:\n3', 3: '', 4: ''}, {0: 'Michel (Elfmeter)\nLinksschuss, Engels', 1: "45'\n+7", 2: '3\n:\n3', 3: '', 4: ''}, {0: 'Vargas\nRechtsschuss, P. Tietz', 1: "76'", 2: '4\n:\n3', 3: '', 4: ''}, {0: '', 1: '', 2: '4\n:\n4', 3: "90'\n+7", 4: 'Cvancara (Elfmeter)\nRechtsschuss, Borges Sanches'}]
        #kicker_goals = [{0: 'Malen\nRechtsschuss, F. Nmecha', 1: "88'", 2: '1\n:\n0', 3: '', 4: ''}]
        home_team = 'MUE'
        away_team = 'MOE'
        goals = self.browser._transform_goals(kicker_goals, home_team, away_team)

        self.assertIsInstance(goals, list)
        self.assertTrue(len(goals) == 2)
        #self.assertEqual("Matthijs de Ligt", goals["name"])
        #self.assertEqual(188, goals["height"])

    def test_get_match_lineup(self):
        self.browser = KickerScraper()
        line_up = self.browser.get_match_lineup(self.url_me)
        self.assertIsInstance(line_up, dict)
        #self.assertTrue(len(match_goals) == 9)

    def test_enrich_scoring_events(self):
        goals = [{'goal_scored_for': 'Bayer 04 Leverkusen', 'scoring_minute': "88'", 'interim_result': '1:0', 'goal_scorer_name': 'Malen', 'is_penalty': False, 'is_own_goal': False, 'bodypart': 'Rechtsschuss', 'assist_provider_name': 'F. Nmecha'}]
        self.browser = KickerScraper()
        goals = self.browser.add_player_ids_to_scoring_events(self.url_mg, goals)
        
        self.assertIsInstance(goals, list)
        self.assertTrue("goal_scorer_id" in goals[0])

    def test_get_scorers_of_match_overview(self):
        goals_info = [
            {0: '', 1: '', 2: '0\n:\n1', 3: "13'", 4: 'Itakura\nKopfball, Honorat'}, {0: '', 1: '', 2: '0\n:\n2', 3: "27'", 4: 'Cvancara\nRechtsschuss, Weigl'}, 
            {0: 'Rexhbecaj\nLinksschuss, Michel', 1: "29'", 2: '1\n:\n2', 3: '', 4: ''}, {0: '', 1: '', 2: '1\n:\n3', 3: "37'", 4: 'Ngoumou\nRechtsschuss, Omlin'}, 
            {0: 'M. Bauer\nRechtsschuss, Demirovic', 1: "41'", 2: '2\n:\n3', 3: '', 4: ''}, {0: 'Michel (Elfmeter)\nLinksschuss, Engels', 1: "45'\n+7", 2: '3\n:\n3', 3: '', 4: ''}, 
            {0: 'Vargas\nRechtsschuss, P. Tietz', 1: "76'", 2: '4\n:\n3', 3: '', 4: ''}, {0: '', 1: '', 2: '4\n:\n4', 3: "90'\n+7", 4: 'Cvancara (Elfmeter)\nRechtsschuss, Borges Sanches'}
        ]

        self.browser = KickerScraper()
        home_team_scorers, away_team_scorers = self.browser.get_match_scorers_overview(goals_info)

        self.assertIsInstance(home_team_scorers, list)
        self.assertIsInstance(away_team_scorers, list)

    def test_calculate_club_codes(self):
        url = "https://www.kicker.de/bundesliga/teams/2023-24"



if __name__ == "__main__":
    sys.path.insert(0, "../src")
    unittest.main()