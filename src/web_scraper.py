import datetime
from datetime import datetime

import random
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from selenium.webdriver.common.by import By

import re

from import_export_json import save_to_json

class WebScraper:

    def __init__(self):
        #self.driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
        CHROMEDRIVER_PATH = ChromeDriverManager().install()
        
        # Define a custom user agent
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"

        chrome_options = Options()
        chrome_options.add_argument('--headless')
    
        # Set the custom User-Agent
        chrome_options.add_argument(f"--user-agent={user_agent}")
    
        self.driver = webdriver.Chrome(
            service=Service(CHROMEDRIVER_PATH),
            options=chrome_options
        )

    
    def tear_down(self):
        self.driver.quit()

    def get_driver(self):
        return self.driver

    def load_page(self, url):
        try:
            print(f"Loading >>> {url}...")
            # Sleep for the random number of seconds so that web page can be build up and human user is simulated
            random_sleep_time = random.randint(2, 5)
            time.sleep(random_sleep_time)
            self.driver.get(url)

            print(f"Done. Loaded page with title '{self.driver.title}'")
            return True
        except Exception as e:
            print(f"Error loading page: {e}")
            return False
        
class KickerScraper(WebScraper):
    club_codes = {}

    def __init__(self):
        super().__init__()

    def get_club_codes(self, competition="Bundesliga", season="2023-24"):
        key = competition[:2] + season[:4]

        print(f"Clubs {key} in cache >>> {(key in KickerScraper.club_codes)}")

        if key not in KickerScraper.club_codes:
            clubs_info = self.get_teams_info_per_competition_and_season()
            club_ids = [club["id"].split("-") for club in clubs_info]

            codes = {}
            for club_split in club_ids:
                for part in club_split:
                    if len(part) > 3:
                        if part[:3].upper() in codes:
                            continue
                        
                        codes[part[:3].upper()] = '-'.join(club_split)
                        break

            swapped_dict = {value: key for key, value in codes.items()}
            KickerScraper.club_codes[key] = swapped_dict

        return KickerScraper.club_codes[key]

    def get_fixture_links(self, url):
        """
        Input: url like: https://www.kicker.de/{competition}}/{spieltag}/{season}]/{matchday}}
        Output: list of urls pointing to the 

        """
        # "https://www.kicker.de/bundesliga/spieltag/2023-24/1"
        fixture_links = []

        try:
            self.load_page(url)

            fixture_elements = self.driver.find_elements(By.XPATH, 
                                                         "//a[@class='kick__v100-scoreBoard kick__v100-scoreBoard--standard ']") 
            for element in fixture_elements:
                link = element.get_attribute("href")
                fixture_links.append(link)

            print(f"Fixture links >>> {fixture_links}")
        except Exception as e:
            print(f"Error getting fixture links: {e}")
        return fixture_links
    
    def get_match_details(self, url):
        """
        """
        match_info = {}
        try:
            self.load_page(url)
            match = self.driver.find_element(By.XPATH, 
                                        "//div[@class='kick__v100-gameCell kick__v100-gameCell--big']")
            
            teams = match.find_elements(By.XPATH, 
                                        "//div[@class='kick__v100-gameCell kick__v100-gameCell--big']/descendant::div[@class='kick__v100-gameCell__team__name']")


            results = match.find_elements(By.XPATH, 
                                        "//div[@class='kick__v100-gameCell kick__v100-gameCell--big']/descendant::div[contains(@class, 'kick__v100-scoreBoard__scoreHolder ')]")
            
            ratings = match.find_elements(By.XPATH, 
                                        "//div[@class='kick__gameinfo kick__module-margin']/child::div")

            links = self.driver.find_elements(By.XPATH, 
                                        "//div[@class='kick__v100-gameCell kick__v100-gameCell--big']/a")

            home_team = teams[0].get_attribute("innerText")
            away_team = teams[1].get_attribute("innerText")
            half_time_score = results[1].get_attribute("innerText").replace('\n', '')
            full_time_score = results[0].get_attribute("innerText").replace('\n', '')
            rating = ratings[0].get_attribute("innerText").split('\n')[0].strip().replace(',', '.')
            man_of_match = ratings[1].get_attribute("innerText").split('\n') #[0].strip() #, rating[1].split('\n')[2]]
            referee = ratings[2].get_attribute("innerText").split('\n')
            home_team_code = links[0].get_attribute("href").split("/")[3]
            away_team_code = links[1].get_attribute("href").split("/")[3]

            fixture_info = self.driver.find_elements(By.XPATH, 
                                                    "//div[@class='kick__gameinfo__item kick__gameinfo__item--game-preview']/descendant::div[contains(@class, 'kick__gameinfo-block')]")
            for element in fixture_info:
                key, value = self._split_to_key_value(element.get_attribute("innerText"))
                match_info[key] = value

            codes = self.get_club_codes()
   
            match_info["home_team"] = home_team
            match_info["home_team_code"] = codes[home_team_code]
            match_info["away_team"] = away_team
            match_info["away_team_code"] = codes[away_team_code]
            match_info["half_time_score"] = half_time_score
            match_info["full_time_score"] = full_time_score

            match_info = self._replace_keys(match_info)
            date, time = self._convert_datetime_string(match_info["date"])

            match_info["date"] = date
            match_info["local_time"] = time

            attendance, is_soldOut = (int(match_info["attendance"].split()[0].replace('.', '')), '(ausverkauft)' in match_info["attendance"])
            match_info["attendance"] = attendance
            match_info["is_soldOut"] = is_soldOut

            match_info["rating"] = rating
            match_info["man_of_match"] = [man_of_match[2], float(re.sub("[^0-9,]", "", man_of_match[4]).replace(",","."))]
            match_info["referee"] = [referee[2], float(re.sub("[^0-9,]", "", referee[4]).replace(",","."))]

            print(f"Match info >>> {match_info}")
        except Exception as e:
            print(f"Error getting match info: {e}")

        return match_info
    
    def get_match_goals_info(self, url):
        """ Navigates to a dedicated match' schema page and gets all scored goals, corresponding scoring minute, scoring team, scorer by name and the assist provider in raw format (as provided on the page).
        >>> browser = KickerScraper()
        >>> url_me = "https://www.kicker.de/augsburg-gegen-mgladbach-2023-bundesliga-4861973/schema"
        >>> match_goals = browser.get_match_goals(url_me)
        >>> title = browser.get_driver().title
        'Spielschema' in title
        >>> count = len(match_goals)
        8
        """
        try:
            self.load_page(url)
            fixture_schema = self.driver.find_elements(By.XPATH, 
                                                      "//div[@class='kick__goals kick__goals--ingame ']/descendant::div[contains(@class, 'kick__goals__row')]")
            
            goal_info = []
            for element in fixture_schema:
                goals = element.find_elements(By.XPATH,
                                            "child::*")
                goal_event = {}
                for i, goal in enumerate(goals):
                    info = goal.get_attribute("innerText")
                    goal_event[i] = info
                        
                goal_info.append(goal_event)      

            #goal_info = self.transform_goals(goal_info, home_team, away_team)          
            #fixture["goals"] = goal_info
            print(f"Goal info >>> {goal_info}")
        except Exception as e:
            print(f"Error getting goals: {e}")
    
        return goal_info
    
    def get_all_per_season(self, url):
        """
        Acts as a controller to create full structure consisting of teams, stadiums, and player profiles
        Steps: 
            1   https://www.kicker.de/bundesliga/teams/2023-24
            2   https://www.kicker.de/bundesliga/spieltag/2023-24/1
            3   
                https://www.kicker.de/bremen-gegen-bayern-2023-bundesliga-4861795/analyse
                https://www.kicker.de/bremen-gegen-bayern-2023-bundesliga-4861795/spielinfo
                https://www.kicker.de/bremen-gegen-bayern-2023-bundesliga-4861795/schema

        """
        bl_season = {}
        # Open browser
        try:
            # bl_season["competition"] = "Bundesliga"
            # bl_season["location"] = "Germany"
            # bl_season["season"] = "2023-24"

            # navigate to bundesliga clubs starting page
            teams_info = self.get_teams_info_per_competition_and_season()
            print(f"Found {len(teams_info)} teams for season {url.split("/")[-1]}")

            teams = []
            players = []
            for team_info in teams_info[:3]:
                # Call each team page and save all team and player information
                team = self.get_team_profile(team_info["info"])

                # Call each stadium page and save all team and player informatio
                stadium = self.get_stadium_info(team_info["stadium"])
            
                # Call all players pages
                players.append(self.get_players_profile_from_team(team_info["squad"]))

                team["stadium"] = stadium
                teams.append(team)
            bl_season["clubs"] = teams
            bl_season["players"] = players

            season_fixtures, goals = self.load_all_fixtures_and_events()
            bl_season["season_fixtures"] = season_fixtures

            # Add 'id' to each dictionary
            for i, goal in enumerate(goals, start=1):
                # Create a new dictionary with the 'id' at the first position
                goals[i-1] = {"id": i, **goal}

            bl_season["goals"] = goals
            print(f"BL season >>> {bl_season}")
        except Exception as e:
            print(f"Error getting all teams: {e}")

        file_path = "bl_2324.json"
        save_to_json(bl_season, file_path)
        return bl_season
        
    def load_all_fixtures_and_events(self, competition="bundesliga", season="2023-24", start=1, stop=35):
        season_fixtures = []
        goals = []
        for md in range(start, stop):
            url = f"https://www.kicker.de/{competition}/spieltag/{season}/{md}"
            fixture_links = self.get_fixture_links(url)
            matchday = {}
            matchday["matchday"] = md
            fixtures = []
            for fixture in fixture_links[:1]:
                match_info = self.get_match_details(fixture.replace('analyse', 'spielinfo'))
                match_goals_info = self.get_match_goals_info(fixture.replace('analyse', 'schema'))
                home_team_scorers, away_team_scorers = self.get_match_scorers_overview(match_goals_info)
                match_info["home_team_scorers"] = home_team_scorers
                match_info["away_team_scorers"] = away_team_scorers

                line_up = self.get_match_lineup(fixture.replace('analyse', 'schema'))
                goals = goals + self.add_player_ids_to_scoring_events(
                    fixture.replace('analyse', 'schema'), 
                    self._transform_goals(match_goals_info, match_info["home_team_code"], match_info["away_team_code"]), line_up)

                team_ratings = self._transform_team_ratings(line_up)
                match_info["team_ratings"] = team_ratings
                fixtures.append(match_info)
            matchday["fixtures"] = fixtures

            season_fixtures.append(matchday)
        
        return season_fixtures, goals

    def get_teams_info_per_competition_and_season(self, url):
        return self.get_teams_info_per_competition_and_season(url.split("/")[3], url.split("/")[-1])

    def get_teams_info_per_competition_and_season(self, competition="bundesliga", season="2023-24"):
        """
        Starts at Kicker page with all teams from a dedicated season for a dedicated competition (eg all teams in 1.Bundesliga, season 2023-24).
        The retunrned dictionary contains all relevant links to teams profile page, to the overview page for players and stadium information page.

        Input: url pointing to the Kicker team info page: https://www.kicker.de/{player}/spieler/{competition}/{season}/{team}
        Output: dictionary containing player attributes as follows: 'name': {player_name}, 'position': {members_count}, 'dateOfBirth': {dateOfBirth}, 'height': {height}, 'weight': {weight}, 
        'nation': {citizenship} 
        {   'name': 'Bayer 04 Leverkusen', 
            'id': 'bayer-04-leverkusen',
            'info': 'https://www.kicker.de/bayer-04-leverkusen/info/bundesliga/2023-24', 
            'squad': 'https://www.kicker.de/bayer-04-leverkusen/kader/bundesliga/2023-24', 
            'stadium': 'https://www.kicker.de/bayer-04-leverkusen/team-stadion/bundesliga/2023-24'}
        """
        clubs_info = []

        try:
            url = f"https://www.kicker.de/{competition}/teams/{season}"
            self.load_page(url)
            club_rows = self.driver.find_elements(By.XPATH, 
                                                "//table[@class='kick__table kick__table--ranking kick__table--alternate kick__table--resptabelle']/descendant::tr")

            for row in club_rows:
                club = {}
                club_cells = row.find_elements(By.XPATH,
                                                 "descendant::td/descendant::a")    

                club['name'] = club_cells[1].get_attribute("innerText")
                club['id'] = club_cells[1].get_attribute("href").split('/')[3]

                for cell in club_cells:        
                    isMemberOf, key = self._validateItem(cell.get_attribute('innerText'))
                    if isMemberOf:
                        club[key] = cell.get_attribute('href')

                clubs_info.append(club)

            print(f"Club info >>> {clubs_info}")
        except Exception as e:
            print(f"Error getting clubs: {e}")
        return clubs_info
    
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
        Gets all relevant dedicated player's data on the Kicker player's profile page 
        Input: url pointing to a Kicker player's profile page: https://www.kicker.de/{player}/spieler/{competition}/{season}/{team}
        Output: dictionary containing player attributes as follows: 'name': {player_name}, 'position': {members_count}, 'dateOfBirth': {dateOfBirth}, 'height': {height}, 'weight': {weight}, 
        'nation': {citizenship} 
        >>> browser = KickerScraper()
        >>> url_player = "https://www.kicker.de/matthijs-de-ligt/spieler/bundesliga/2023-24/fc-bayern-muenchen"
        >>> player = browser.get_player_info(url_player)
        """
        player_info = {}

        try:
            codes = self.get_club_codes()

            self.load_page(url)
            name = self.driver.find_element(By.XPATH, 
                                                "//div[@class='kick__vita__header__person-name-medium-h1']").get_attribute("innerText")
            first_name =  self.driver.find_element(By.XPATH, 
                                                "//div[@class='kick__vita__header__person-name-medium-h1']/span").get_attribute("innerText")

            last_name =  name.replace(first_name, '').strip()
            
            try:
                current_team = self.driver.find_element(By.XPATH,
                                                    "//div[@class='kick__vita__header__team-name']").get_attribute("innerText")
            except:
                current_team = "NA"

            player_info["id"] = url.split("/")[3]
            name = name.split("(")
            if(len(name) == 1):
                name = name[0].strip()
            else:
                name = name[1].replace(")", '')

            player_info["name"] = name
            
            player_info["first_name"] = first_name.split("(")[0].strip()
            player_info["last_name"] = last_name
            
            team_id = url.split("/")[-1]
            player_info["club_code"] = codes[team_id]
            player_info["team_id"] = team_id
            player_info["current_team"] = current_team.strip()

            player_details = self.driver.find_elements(By.XPATH,
                                                ("//div[contains(@class,'kick__vita__header__person-detail-kvpair-info')]"))

            for pd in player_details:
                item = pd.get_attribute("innerText")
                if ":" in item:
                    value = item.split(':')[1].strip().split()[0]
                    if value.isdigit():
                        value = int(value)
                    player_info[item.split(':')[0].strip()] = value 

            player_info = self._replace_keys(player_info)
            print(f"Player details >>> {player_info}")
        except Exception as e:
            print(f"Error getting player info: {e}")

        return player_info

    def get_team_profile(self, url):
        """
        Input: url pointing to the Kicker team info page: https://www.kicker.de/{team}/info/{competition}/{season}
        Output: dictionary containing team attributes as follows: 'name': {team_name}, 'members': {members_count}, 'url': {url_to_kicker_info_page}, 'slug': {slugified_team_name}, '' 
        """
        team = {}

        name = 'NA'
        members = -1
        try:
            self.load_page(url)
            team_info = self.driver.find_elements(By.XPATH, 
                                                "//div[@class='kick__data-list']/child::div/div[@class='kick__data-list__value']") 
            team["name"] = team_info[0].get_attribute("innerText")
            team["members"] = (int(team_info[2].get_attribute("innerText").split()[0].replace('.', '')))
            #team["url"] = url
            team["id"] = url.split('/')[3]

            manager_info = self.driver.find_elements(By.XPATH, 
                                                "//div[@class='kick__portrait-photo-holder']//img") 
            if(len(manager_info) >= 2):
                team["manager"] = manager_info[0].get_attribute("alt")
                team["manager_nationality"] = manager_info[1].get_attribute("alt")

            print(f"Team info >>> {team}")
        except Exception as e:
            print(f"Error getting team info: {e}")

        return team
    

    def get_stadium_info(self,url):
        """Gets stadium info from the page. 
        >>> browser = KickerScraper()
        >>> url_stadium = "https://www.kicker.de/fc-bayern-muenchen/team-stadion/bundesliga/2024-25"
        >>> stadium = browser.get_stadium_info(url_stadium)
        """
        stadium = {}

        name = 'NA'
        totalCapacity = -1
        try:
            self.load_page(url)            
            name = self.driver.find_element(By.XPATH, 
                                        "//div[@class='kick__profile-data__grid-icon kick__site-padding']").get_attribute("innerText")

            stadium["name"] = name.split("\n")[0]
            stadium_info = self.driver.find_elements(By.XPATH, 
                                                    "//td[@class='kick__t__a__l']/following-sibling::td") 

            stadium["totalCapacity"] = int(stadium_info[0].get_attribute("innerText").replace('.', ''))

            print(f"Stadium details >>> {stadium}")
        except Exception as e:
            print(f"Error getting stadium info: {e}")

        return stadium
    
    def get_match_lineup(self,url):
        """Gets line-up of home and away team on the match schema page. Contains player's name and id, team id and also player's rating for that match.
        Input: url to a concrete    >   match https://www.kicker.de/{fixture_name}/schema
        Output: dictionary with player's name and id, team id and also player's rating for that match. If no rating available -1 is returned for that player. 
        """
        line_up = {}

        try:
            self.load_page(url)            
            all_players = self.driver.find_elements(By.XPATH, 
                                                "//div[@class='kick__card ']/div[@class='kick__site-padding']//a")

            for player in all_players:
                href = player.get_attribute("href") # https://www.kicker.de/{player}/spieler/{competition}/{season}/{team}
                if("spieler" in href):
                    name = re.sub("[0-9,]", "", player.get_attribute("innerText")).strip()
                    id = href.split("/")[3]
                    rating = re.sub("[^0-9,]", "", player.get_attribute("innerText")).replace(",", ".")
                    team_id = href.split("/")[-1]
                    line_up.setdefault(name, [id, team_id, float(rating) if rating != '' else -1]) # no duplicates

            print(f"Match line-up details >>> {line_up}")
        except Exception as e:
            print(f"Error getting match line-up: {e}")

        return line_up
    
    def add_player_ids_to_scoring_events(self, url, goals, line_up=[]):
        """
        Add the player IDs to scorer and assist giving players in the goal / assist list
        """
        if not line_up:
            line_up = self.get_match_lineup(url)

        for goal in goals:
            if goal["goal_scorer_name"] in line_up:
                goal["goal_scorer_id"] = line_up[goal["goal_scorer_name"]][0]

            if ("assist_provider_name" in goal) and (goal["assist_provider_name"] in line_up):
                goal["goal_assist_provider_id"] = line_up[goal["assist_provider_name"]][0]

        print(f"Enriched goal events >>> {goals}")
        return goals
    
    def get_match_scorers_overview(self, goals):
        home_team_scorers, away_team_scorers = [], []
        scorers = []
        for goal in goals:
            if len(goal[0]) > 0:
                l = list(goal.values())[:2]
                l.insert(0, "home")
            else:
                l = list(reversed(goal.values()))[:2]
                l.insert(0, "away")
            
            scorers.append(l)

        for s in scorers:
            s[1] = s[1].split('\n')[0].replace('Elfmeter', ('P')).replace('Eigentor', 'O') + " " + s[2].replace('\n', '')
            #print(scorer_info)

        [home_team_scorers.append(l[1]) if l[0] == 'home' else away_team_scorers.append(l[1]) for l in scorers]

        print(f"{home_team_scorers} >>> {away_team_scorers}")

        return home_team_scorers, away_team_scorers
    
    def _transform_team_ratings(self, line_up):
        result = {}

        for key, value in line_up.items():
            if(value[2] == -1):
                continue
            club = value[1]  # Get the club id (second element)
            player_data = [value[0], value[2]]  # Get player id and rating
            
            if club not in result:
                result[club] = []
            result[club].append(player_data)
        return result
    
    def _validateItem(self, key):
            keys = ['info', 'squad', 'stadium']
            if(key in ['', 'Kader', 'Stadion']):
                key = keys[['', 'Kader', 'Stadion'].index(key)]
                isMemberOf = True
            else:
                isMemberOf = False

            return isMemberOf, key

    def _split_to_key_value(self, data):
        # Split the string at '\n'
        parts = data.split('\n')
        if len(parts) == 2:  # Ensure that there are exactly two parts after splitting
            key = parts[0].strip()
            value = parts[1].strip()

        return key, value
    
    def _replace_keys(self, my_dict):
        # Dictionary mapping old keys to new keys
        key_mapping = {
            'Anstoß': 'date',
            'Stadion': 'venue',
            'Zuschauer': 'attendance',
            'Position': 'position',
            'Geboren': 'dateOfBirth',
            'Größe': 'height',
            'Gewicht': 'weight',
            'Nation': 'nationality'
        }

        # Replace keys in the original dictionary
        for old_key, new_key in key_mapping.items():
            if old_key in my_dict:
                my_dict[new_key] = my_dict.pop(old_key)
        
        return my_dict
    
    # Function to convert the input string to desired format
    def _convert_datetime_string(self, dt_string):
        dt_obj = datetime.strptime(dt_string[2:], "%d.%m.%Y, %H:%M")

        weekday_abbr = dt_string[:2]
        weekday = weekday_abbr + dt_obj.strftime(", %d.%m.%Y")
        time = dt_obj.strftime("%H:%M")    
        return weekday, time

    def _transform_goals(self, goals, home_team, away_team):
        """ Transforms a list of goals as provided by the Kicker page on https://www.kicker.de/{fixture}/schema
        Input: 
        goals> list of goals as provided on Kicker page in the form of: 
            [{0: '', 1: '', 2: '0\n:\n1', 3: "13'", 4: 'Itakura\nKopfball, Honorat'}, {0: 'Rexhbecaj\nLinksschuss, Michel', 1: "29'", 2: '1\n:\n1', 3: '', 4: ''}]
        home_team, away_team: name of home and away teams in this fixture
        Output: list of goal dictionaries: 'name': {team_name}, 'members': {members_count}, 'url': {url_to_kicker_info_page}, 'slug': {slugified_team_name}, '' 

        Special treatment of Eigentor, Elfmeter, 

        Gets a list of goals in the form of as desribed in the next test cases:
        >>> browser = KickerScraper()
        >>> td_goals = [{0: '', 1: '', 2: '0\\n:\\n1', 3: "13'", 4: 'Itakura\\nKopfball, Honorat'}, {0: '', 1: '', 2: '0\\n:\\n2', 3: "27'", 4: 'Cvancara\\nRechtsschuss, Weigl'}, {0: 'Rexhbecaj\\nLinksschuss, Michel', 1: "29'", 2: '1\\n:\\n2', 3: '', 4: ''}, {0: '', 1: '', 2: '1\\n:\\n3', 3: "37'", 4: 'Ngoumou\\nRechtsschuss, Omlin'}, {0: 'M. Bauer\\nRechtsschuss, Demirovic', 1: "41'", 2: '2\\n:\\n3', 3: '', 4: ''}, {0: 'Michel (Elfmeter)\\nLinksschuss, Engels', 1: "45'\\n+7", 2: '3\\n:\\n3', 3: '', 4: ''}, {0: 'Vargas\\nRechtsschuss, P. Tietz', 1: "76'", 2: '4\\n:\\n3', 3: '', 4: ''}, {0: '', 1: '', 2: '4\\n:\\n4', 3: "90'\\n+7", 4: 'Cvancara (Elfmeter)\\nRechtsschuss, Borges Sanches'}]
        >>> goals = browser.transform_goals(td_goals, "home", "away")
        >>> count = len(goals)
        8
        """
        transformed_goals = []
        print(f"Goals   >>> {goals}")
        for goal in goals:
            new_goal = {}

            new_goal["home_team"] = away_team
            new_goal["away_team"] = away_team

            # Determine if goal was scored for home or away team
            if goal[0] == '':
                new_goal["goal_scored_for"] = away_team
                new_goal["scoring_minute"] = goal[3].replace('\n', '')  # Use goal["3"] for away_team
                scorer_info = goal[4]  # Use goal["4"] for away_team
            else:
                new_goal["goal_scored_for"] = home_team
                new_goal["scoring_minute"] = goal[1].replace('\n', '')  # Use goal["1"] for home_team
                scorer_info = goal[0]  # Use goal["0"] for home_team
            
            # Map the interim_result and remove "\n"
            new_goal["interim_result"] = goal[2].replace('\n', '')
            
            # Transform scorer_info
            if scorer_info:
                scorer_parts = scorer_info.split('\n', 1)  # Split on the first '\n' if exists

                new_goal["goal_scorer_name"] = re.split(r'\(Elfmeter\)|\(Eigentor\)', scorer_parts[0])[0].strip()
                #new_goal["goal_scorer_name"] = scorer_parts[0].split(' (Elfmeter)')[0]  # Remove '(Elfmeter)' if exists

                new_goal["is_penalty"] = '(Elfmeter)' in scorer_parts[0]
                new_goal["is_own_goal"] = '(Eigentor)' in scorer_parts[0]
                
                #new_goal["goal_scorer_name"] = scorer_parts[0].split(' (Eigentor)')[0]  # Remove '(Eigentor)' if exists

                if len(scorer_parts) > 1:
                    bodypart_and_assist = scorer_parts[1].split(', ')
                    new_goal["bodypart"] = bodypart_and_assist[0]  # First part after '\n'
                    
                    if len(bodypart_and_assist) > 1:
                        new_goal["assist_provider_name"] = bodypart_and_assist[1]  # After the comma
                    
            # Add to the transformed goals list
            transformed_goals.append(new_goal)

        print(f"Transformed goals >>> {transformed_goals}")
        return transformed_goals

if __name__ == '__main__':
    import doctest
    doctest.testmod(verbose=True)