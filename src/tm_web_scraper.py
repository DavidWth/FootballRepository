from web_scraper import WebScraper
import datetime
from datetime import datetime

import random
import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException

import re

from import_export_json import save_to_json
        
class TransfermarktScraper(WebScraper):
    def __init__(self):
        super().__init__()
    
    def get_matchday_details(self, url):
        """
        Transfermarkt > Season/Matchday > Matchday 1-n
        Prepares a whole matchday using: "https://www.transfermarkt.com/bundesliga/spieltag/wettbewerb/L1/saison_id/2023/spieltag/1"
        """
        match_events = []
        try:
            self.load_page(url)
            all_matches = self.driver.find_elements(By.XPATH, 
                                            "//div[@class='box']/table[@style='border-top: 0 !important;']/child::tbody")
            

            for match in all_matches:
                details = match.find_elements(By.XPATH, "child::tr")
                events = []
                for row in details:
                    if len(row.get_attribute('innerText')) >= 1:
                        #events.append(row.get_attribute('innerText').replace('\xa0', ' ').replace('\t', ' ').strip())
                        events.append(row.get_attribute('innerText'))
                        print(f"Match info >>> {row.get_attribute('innerText').strip()}")

                match_events.append(events)
            print(f"Match info >>> {match_events}")
        except Exception as e:
            print(f"Error getting match info: {e}")

        return match_events
    
    def get_match_details(self, url):
        """
        Transfermarkt > Match Sheet > Fixture info
        Data: Teams, Matchday, Date, result (interim)
        https://www.transfermarkt.com/spielbericht/index/spielbericht/4095967
        """
        match_details = []
        try:
            self.load_page(url)
            match_details = self.driver.find_elements(By.XPATH, 
                                            "//div[@class='box-content']/child::div/child::*")
            

            for match in match_details:
                match_details.append(match.get_attribute("innerText"))

            print(f"Match info >>> {match_details}")
        except Exception as e:
            print(f"Error getting match info: {e}")

        return match_details
    
    def get_goals_details_per_match(self, url):
        """

        https://www.transfermarkt.com/spielbericht/index/spielbericht/4095967
        "//div[@id='sb-tore']/ul/li/child::div/child::div"
        """
        goals_details = []
        try:
            self.load_page(url)
            goals_elements = self.driver.find_elements(By.XPATH, 
                                            "//div[@id='sb-tore']/ul/li/child::div")

            for elements in goals_elements:
                rows = elements.find_elements(By.XPATH, "child::div")
                goal_detail = []
                for goal in rows:
                    goal_detail.append(goal.get_attribute('innerText'))
                    #print(f"Goals details >>> {goal.get_attribute('innerText')}")
                goals_details.append(goal_detail)

            print(f"Goal info >>> {goals_details}")
        except Exception as e:
            print(f"Error getting match info: {e}")

        return goals_details
    
    def get_top_players_per_match(self, url):
        """
        https://www.transfermarkt.com/spielbericht/index/spielbericht/4095967
        "//div[@id='sb-tore']/ul/li/child::div/child::div"
        """
        top_players = []
        try:
            self.load_page(url)
            top_players_divs = self.driver.find_elements(By.XPATH, 
                                            "//div[@id='sb-notenbeste']/descendant::li/child::div")
            

            for goal in top_players_divs:
                top_players.append(goal.get_attribute('innerText'))

            print(f"Top players in match >>> {top_players}")
        except Exception as e:
            print(f"Error getting match info: {e}")

        return top_players
    
    def get_player_ratings_per_match(self, url):
        """
        Transfermarkt > Line-Ups > Line-Up tables

        https://www.transfermarkt.com/bayer-04-leverkusen_rb-leipzig/aufstellung/spielbericht/4095970
        "//div[@class='box']/div[@class='responsive-table']/table/tbody/tr/child::td" > tr
        """
        player_ratings = []
        try:
            self.load_page(url)
            player_ratings_rows = self.driver.find_elements(By.XPATH, 
                                            "//div[@class='box']/div[@class='responsive-table']/table/tbody/tr")
            
            for row in player_ratings_rows:
                details = row.find_elements(By.XPATH, "child::td")
                events = []
                for cell in details:
                    if len(cell.get_attribute('innerText')) >= 1:
                        events.append(cell.get_attribute('innerText'))
                player_ratings.append(events)

            print(f"Goal info >>> {player_ratings}")
        except Exception as e:
            print(f"Error getting match info: {e}")

        return player_ratings
    
        
    def get_teams_info_per_competition_and_season(self, url):
        """
        Transfermarkt > Season > all participating clubs
        
        Input: url pointing to Transfermarkt teams overview page per season: https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1/plus/?saison_id=2023
        Output: list of dictionaries containing clubs name and url: 'name': {team_name}, 'url': {team_url} 
        {   'name': 'Bayern Munich', 
            'url': 'https://www.transfermarkt.com/fc-bayern-munchen/startseite/verein/27/saison_id/2023,
        }
        """
        clubs_info = []

        try:
            self.load_page(url)
            club_rows = self.driver.find_elements(By.XPATH, 
                                                "//div[@id='yw1']//tbody/tr/td[@class='hauptlink no-border-links']/a[1]")

            for row in club_rows:
                club = {}

                href = row.get_attribute("href")

                club['name'] = row.get_attribute("innerText")
                club['url'] = href
                clubs_info.append(club)
                
            print(f"Club info >>> {clubs_info}")
        except Exception as e:
            print(f"Error getting clubs: {e}")
        return clubs_info
    
    def get_club_portrait(self, url):
        """
        Transfermarkt > Club Portrait > Stats & Facts

        Input: url pointing to the Kicker team info page: https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1/plus/?saison_id=2023
        Output: dictionary containing player attributes as follows: 'name': {player_name}, 'position': {members_count}, 'dateOfBirth': {dateOfBirth}, 'height': {height}, 'weight': {weight}, 
        'nation': {citizenship} 
        {   'name': 'Bayer 04 Leverkusen', 
            'id': 'bayer-04-leverkusen',
            'info': 'https://www.kicker.de/bayer-04-leverkusen/info/bundesliga/2023-24', 
            'squad': 'https://www.kicker.de/bayer-04-leverkusen/kader/bundesliga/2023-24', 
            'stadium': 'https://www.kicker.de/bayer-04-leverkusen/team-stadion/bundesliga/2023-24'}
        """
        # https://www.transfermarkt.com/fc-bayern-munchen/datenfakten/verein/27

        clubs_portrait = {}

        try:
            self.load_page(url)
            club_rows = self.driver.find_elements(By.XPATH, 
                                                "//table[@class='profilheader']/tbody/child::tr/child::*")

            for i in range(0, len(club_rows), 2):
                clubs_portrait[club_rows[i].get_attribute("innerText")] = club_rows[i+1].get_attribute("innerText")
                
            print(f"Club portrait >>> {clubs_portrait}")
        except Exception as e:
            print(f"Error getting club portrait: {e}")
        return clubs_portrait


    def get_stadium_overview(self, url):
        """
        Starts at Kicker page with all teams from a dedicated season for a dedicated competition (eg all teams in 1.Bundesliga, season 2023-24).
        The retunrned dictionary contains all relevant links to teams profile page, to the overview page for players and stadium information page.

        Input: url pointing to the Kicker team info page: https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1/plus/?saison_id=2023
        Output: dictionary containing player attributes as follows: 'name': {player_name}, 'position': {members_count}, 'dateOfBirth': {dateOfBirth}, 'height': {height}, 'weight': {weight}, 
        'nation': {citizenship} 
        {   'name': 'Bayer 04 Leverkusen', 
            'id': 'bayer-04-leverkusen',
            'info': 'https://www.kicker.de/bayer-04-leverkusen/info/bundesliga/2023-24', 
            'squad': 'https://www.kicker.de/bayer-04-leverkusen/kader/bundesliga/2023-24', 
            'stadium': 'https://www.kicker.de/bayer-04-leverkusen/team-stadion/bundesliga/2023-24'}
        """
        # https://www.transfermarkt.com/fc-bayern-munchen/stadion/verein/27/saison_id/2024

        clubs_info = []

        try:
            self.load_page(url)
            club_rows = self.driver.find_elements(By.XPATH, 
                                                "//div[@id='yw1']//tbody/tr/td[@class='hauptlink no-border-links']/a[1]")

            for row in club_rows:
                club = {}

                href = row.get_attribute("href")
                club['name'] = row.get_attribute("innerText")
                club['url'] = href
                clubs_info.append(club)
                
            print(f"Club info >>> {clubs_info}")
        except Exception as e:
            print(f"Error getting clubs: {e}")
        return clubs_info
    
    def get_all_players_from_team(self, url):
        """
        Transfermarkt > club squad page > player's urls.
        Returns list with links/urls for all players in the squad.

        Input: url pointing to a Transfermarkt club page with squad for a season: https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1/plus/?saison_id=2023
        Output: list containing urls to all players per club pages: ['url_1', 'url2', ...] 
        ['https://www.transfermarkt.com/manuel-neuer/profil/spieler/17259', 'https://www.transfermarkt.com/daniel-peretz/profil/spieler/468539', ...]
        """
        # https://www.transfermarkt.com/bayern-munich/kader/verein/27/saison_id/2024/plus/1

        players_urls = []

        try:
            self.load_page(url)
            player_rows = self.driver.find_elements(By.XPATH, 
                                                "//div[@id='yw1']//td[@class='hauptlink']/a")

            for player in player_rows:
                players_urls.append(player.get_attribute("href"))

            print(f"Players' urls >>> {players_urls}")
        except Exception as e:
            print(f"Error getting clubs: {e}")
        return players_urls
    
    def get_players_profile_from_team(self, url):
        """
        Orchestrates data retrieval starting from a team's squad overview page and then navigating to each player's profile page 
        Input   >   https://www.kicker.de/{team}/kader/{competition}/{season}
        Output  >   list of all players' profile from a dedicated team
        """
        players_info = self.get_players_info_from_team(url)

        urls = [item['url'] for item in players_info if 'url' in item]

        players = []
        for player_url in urls:
            players.append(self.get_player_profile_from_team(player_url))

        print(f"All players from {url.split('/')[3]} >>> {players}")
        return players

    def get_players_info_from_team(self, url):
        """
        Input: url pointing to the Kicker team info page: https://www.kicker.de/{player}/spieler/{competition}/{season}/{team}
        Output: dictionary containing player attributes as follows: 'name': {player_name}, 'position': {members_count}, 'dateOfBirth': {dateOfBirth}, 'height': {height}, 'weight': {weight}, 
        'nation': {citizenship} 
        >>> browser = KickerScraper()
        >>> url_player = "https://www.kicker.de/matthijs-de-ligt/spieler/bundesliga/2023-24/fc-bayern-muenchen"
        >>> player = browser.get_player_info(url_player)
        """
        players_info = []

        try:
            self.load_page(url)
            player_rows = self.driver.find_elements(By.XPATH, 
                                                "//div[@class='kick__data-grid__main ']/descendant::tbody/tr/descendant::a")

            for row in player_rows:
                player_info = {}

                player_info['id'] = row.get_attribute("href").split('/')[3]
                player_info['name'] = row.get_attribute("innerText")
                player_info['url'] = row.get_attribute("href")

                players_info.append(player_info)

            print(f"Players info >>> {players_info}")
        except Exception as e:
            print(f"Error getting players info: {e}")
        return players_info
    
    def get_player_profile_from_team(self, url):
        """
        Transfermarkt > Player profile page > Player data
        Input
        Output
        """
        # https://www.transfermarkt.com/alphonso-davies/profil/spieler/424204
        player_profile = {}

        try:
            self.load_page(url)

            name_and_number = self.driver.find_element(By.XPATH, 
                                                "//h1[@class='data-header__headline-wrapper']")
            
            player_profile["name_and_jersey"] = name_and_number.get_attribute("innerText")
            name_info = name_and_number.find_elements(By.XPATH, 
                                                "//h1[@class='data-header__headline-wrapper']/descendant::*")
            player_profile["jersey_number"] = name_info[0].get_attribute("innerText")
            player_profile["last_name"] = name_info[1].get_attribute("innerText")

            player_data = self.driver.find_elements(By.XPATH, 
                                                "//div[@class='info-table info-table--right-space ']/child::span")
            
            for i in range(0, len(player_data), 2):
                player_profile[player_data[i].get_attribute('innerText')] = player_data[i+1].get_attribute('innerText')


            player_profile["url"] = url
            
            print(f"Player details >>> {player_profile}")
        except Exception as e:
            print(f"Error getting player info: {e}")

        except Exception as e:
            print(f"Error getting market value: {e}")

        return player_profile
    
    def get_player_stats_from_team(self, url):
        """
        Transfermarkt > Player stats page > Stats per season and competition
        Input
        Output  dictionary continaing player statistics
        """
        # https://www.transfermarkt.com/jamal-musiala/leistungsdaten/spieler/580195/plus/0?saison=2023
        player_stats = {}

        try:
            self.load_page(url)
            player_stats_headers = self.driver.find_elements(By.XPATH, 
                                                "//table[@class='items']/thead/tr/th")
            player_stats_x = self.driver.find_elements(By.XPATH, 
                                                "//table[@class='items']/tbody/tr[1]/child::*")

            for header, stats in zip(player_stats_headers, player_stats_x):
                if len(header.get_attribute("innerText")) <= 1:
                    title = header.find_element(By.XPATH, "descendant::span").get_attribute("title")
                else:
                    title = header.get_attribute("innerText")
        
                if len(stats.get_attribute("innerText")) == 0:
                    value = stats.find_element(By.XPATH, "child::*[1]").get_attribute("title")
                else:
                    value = stats.get_attribute("innerText")
                
                player_stats[title] = [value]
    
            print(f"Player stats >>> {player_stats}")
        except Exception as e:
            print(f"Error getting player stats: {e}")

        return player_stats_x
    
    def get_market_values(self, url):
        """
        Transfermarkt > Player profile > Market value
        https://www.transfermarkt.com/jamal-musiala/profil/spieler/580195
        """
        try:
            self.load_page(url)
        except Exception as e:
            print(f"Error getting market values: {e}")
        
        # Wait for the iframe containing the button, if any, and switch to it
        try:
            iframe = WebDriverWait(self.driver, 8).until(
                EC.presence_of_element_located((By.ID, "sp_message_iframe_953358"))  # Adjust the selector if needed
            )
            self.driver.switch_to.frame(iframe)
        except TimeoutException as e:
            pass  # No iframe found, proceed without switching

        # Wait for the button to be clickable
        try:
            button = WebDriverWait(self.driver, 4).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, ".message-component.message-button.no-children.focusable.accept-all.sp_choice_type_11.first-focusable-el"))
            )

            # Click the button
            button.click()
        except TimeoutException as e:
            pass  # No iframe found, proceed without switching

        last_height = self.driver.execute_script("return document.body.scrollHeight")
    
        while True:
            # Scroll down by 1000 pixels
            self.driver.execute_script("window.scrollBy(0, 750);")
                
            # Wait for the page to load new content
            time.sleep(2)
                
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
                
            if new_height == last_height:
                break  # Break the loop if no new content is loaded
                
            last_height = new_height
        
        try:
            market_values = []
            market_value = self.driver.find_elements(By.XPATH, 
                                                 "//div[@class='current-and-max svelte-18lvpom']/child::div/child::div")

            for mv in market_value:
                market_values.append(mv.get_attribute("innerText"))

            print(f"Market_values >>> {market_values}")
        except Exception as e:
            print(f"Error getting market value: {e}")

        return market_values
    
    
    def _click_button_in_iframe(self, iframe="sp_message_iframe_953358", css_selector=".message-component.message-button.no-children.focusable.accept-all.sp_choice_type_11.first-focusable-el"):
        # Wait for the iframe containing the button, if any, and switch to it
        try:
            iframe = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, iframe))  # Adjust the selector if needed
            )
            self.driver.switch_to.frame(iframe)
        except TimeoutException as e:
            pass  # No iframe found, proceed without switching

        # Wait for the button to be clickable
        try:
            button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector))
            )

            # Click the button
            button.click()
        except TimeoutException as e:
            pass  # No iframe found, proceed without switching

        # Switch back to the default content if you switched to an iframe
        self.driver.switch_to.default_content()
        return
    
    def _scroll_current_page(self, start=0, stop=750):
        last_height = self.driver.execute_script("return document.body.scrollHeight")
    
        while True:
            # Scroll down by 1000 pixels
            self.driver.execute_script("window.scrollBy(0, 750);")
                
            # Wait for the page to load new content
            time.sleep(3)
                
            # Calculate new scroll height and compare with last scroll height
            new_height = self.driver.execute_script("return document.body.scrollHeight")
                
            if new_height == last_height:
                break  # Break the loop if no new content is loaded
                
            last_height = new_height
 
        return

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)