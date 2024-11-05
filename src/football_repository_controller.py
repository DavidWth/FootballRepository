from tm_web_scraper import TransfermarktScraper
from import_export_json import *
from datetime import date
import time
import configparser

class FootballRepositoryController():
    competitions = { #existing competitions and mapped tiers
        "bundesliga": "L1",
        "2-bundesliga": "L2"
    }

    clubs_processing = {
        0: "https://www.transfermarkt.com/{name}/{startseite}/verein/{id}/saison_id/{season}",
        1: "datenfakten",   #   https://www.transfermarkt.com/fc-bayern-munchen/datenfakten/verein/27
        2: "stadion",       #   https://www.transfermarkt.com/fc-bayern-munchen/stadion/verein/27
    }



    config_file = {
        "clubs": "clubs_info.json",
        "portraits": "clubs_portraits.json"
    }


    seasons = [2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 
               2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 
               2022, 2023, 2024]
    
    clubs_info = None
    clubs_portraits = None

    def _load_clubs_info(self, repository, update:bool=False):
        if(repository is None or update==True):
            try:
                self.clubs_info = load_from_json(self.config_file["clubs"])
                print(f"Loaded {len(self.clubs_info) if isinstance (self.clubs_info, dict) else 0} competitions into repository.")
            except FileNotFoundError:
                print(f"1 File {self.config_file["clubs"]} does not exist, no clubs loaded yet.")
            finally:
                print(f"2 File {self.config_file["clubs"]} does not exist, no clubs loaded yet.")

        # check if there are values in the repository, if not load file, if yes load only if update=True

        return repository
    
    def _load_clubs_portraits(self, update:bool=False):
        if(self.clubs_portraits is None or update==True):
            try:
                self.clubs_portraits = load_from_json(self.config_file["portraits"])
                print(f"Loaded {len(self.clubs_portraits) if isinstance (self.clubs_portraits, dict) else 0} competitions into repository.")
            except FileNotFoundError:
                print(f"1 File {self.config_file["portraits"]} does not exist, no clubs loaded yet.")
            finally:
                print(f"2 File {self.config_file["portraits"]} does not exist, no clubs loaded yet.")

        # check if there are values in the repository, if not load file, if yes load only if update=True

        return self.clubs_portraits
    
    def get_club_urls(self, competition, season):

        return "urls"

    def __init__(self):
        #super().__init__()
        self.config = configparser.ConfigParser()
        self.config.read('config/config.ini')

        self.browser = TransfermarktScraper()
        self.mappings = load_from_json("config\\keys_mapping.json")
        self._load_clubs_info(repository=self.clubs_info)
        print(self.mappings)

    def crawl_and_save_clubs(self, competition="bundesliga", season="2023", overwrite=False):
        """
        Get club details from Transfermarkt pages and save them to json files as raw data.

        """
        # https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1/plus/?saison_id=2024
        # https://www.transfermarkt.com/bundesliga/startseite/wettbewerb/L1/plus/?saison_id=2023
        # https://www.transfermarkt.com/2-bundesliga/startseite/wettbewerb/L2/plus/?saison_id=2024

        url_templates = self.config.get("URLTEMPLATES", "clubs_url"),

        now = str(date.today()).replace("-", "")

        clubs_x_season_url = self.url_templates.format(competition=competition, tier="L1", season=season)
        clubs_info = self.browser.get_teams_info_per_competition_and_season(clubs_x_season_url)
        save_to_json(clubs_info, f"clubs_bundesliga_{season}_{now}.json")
        self._load_clubs_info(update=True)

        # club_urls = [club["url"].replace("startseite", "datenfakten") for club in clubs_info]
        # for club in club_urls:
        #     print(f"URL >>  {club}")

        # clubs = []
        # for club in club_urls:
        #     clubs.append(self.browser.get_club_portrait(club))

        # save_to_json(clubs, f"clubportrait_bundesliga_{season}_{now}.json", "w")

        # club_urls = [club["url"].replace("startseite", "stadion") for club in clubs_info]
        # for club in club_urls:
        #     print(f"URL >>  {club}")

        # stadiums = []
        # for club in club_urls:
        #     stadiums.append(self.browser.get_club_portrait(club))

        # save_to_json(stadiums, f"stadiums_bundesliga_{season}_{now}.json", "w")

    def parse_season_data(self):
        
        pass

    def scrape_and_save_club_infos(self, season:str, competition:str, overwrite:bool):
        # UC: Prepare the clubs urls for further navigation. The user can provide the competition and season, this combination is used for storing the urls in a file for later use.
        # Information which is already in the file will not be scraped again to prevent costly roundtrips. But this behaviour can be overruled.
        # Scenario
        # 1 check param validity
        # 2 check if competition + season is already existing in repository
        # 21 precondition: repository must already been loaded
        # If information already there return, else go for web scraping information and save to file

        # 1 check param validity
        if int(season) in range(2000, 2025) and competition in self.competitions:
            print(True)

            # load data into repository (or check if already loaded)
            self.clubs_info = self._load_clubs_info(repository=self.clubs_info)

            # 2 check if competition + season is already existing in repository
            if self.clubs_info and competition in self.clubs_info and season in self.clubs_info[competition]:
                # all good
                teams  = self.clubs_info[competition][season]
                print(f"{competition} found with {teams["teams"]} teams")

                return teams["clubs_info"]            
            else:
                # get data web for this competition, season
                print(f"{competition}-{season} not found.")
                if self.clubs_info is None:
                    self.clubs_info = {}
                    print(f"Clubs data   >>> {type(self.clubs_info)}")

                url_templates = self.config.get("URLTEMPLATES", "clubs_url")
                url = url_templates.format(competition=competition, tier=self.competitions[competition], season=season)
                print(f"Going to    >>> {url}")

                clubs_info = self.browser.get_teams_info_per_competition_and_season(url)

                print(f"Clubs data   >>> {type(self.clubs_info)}")
                # add new structure to overall structure
                if clubs_info:
                    if competition not in self.clubs_info:
                        self.clubs_info[competition] = {}
                    club = {}
                    club = {
                        "teams": len(clubs_info),
                        "clubs_info": clubs_info,
                    }
                    self.clubs_info[competition][season] = club

                print(f"Clubs data   >>> {self.clubs_info}")

                save_to_json(self.clubs_info, "clubs_info.json")

                return clubs_info
        else:
            raise ValueError(f'Season {season} must be between 2000 and 2024')
        
    def scrape_and_save_club_details(self, season:str, competition:str, overwrite:bool=False):
        # UC: we have the urls of all clubs per competition and season. we want to load them but only if not already existing.
        # idea is to check on club level, not on season level
        # 1 check param validity
        if int(season) in range(2000, 2025) and competition in self.competitions:
            # 2 check if competition and season available in clubs info repository, (if not reload repository?)
            if self.clubs_info and competition in self.clubs_info and season in self.clubs_info[competition]:
                clubs  = self.clubs_info[competition][season]
                print(f"{competition} found with {clubs["teams"]} teams")

                club_urls = [club["url"] for club in clubs["clubs_info"]]
                club_urls = [club.replace("startseite", "datenfakten") for club in club_urls]

                #21 check if club has already been loadad
                self.clubs_portraits = self._load_clubs_portraits()

                urls = []
                # 'https://www.transfermarkt.com/fc-bayern-munchen/datenfakten/verein/27/saison_id/2024'
                if self.clubs_portraits and competition in self.clubs_portraits and season in self.clubs_portraits[competition]:
                    portraits = self.clubs_portraits[competition][season] 
                    urls = [item['url'] for item in portraits["clubs_info"] if 'url' in item]
                    print(urls)

                if self.clubs_portraits is None:
                    self.clubs_portraits = {}
                
                self.clubs_portraits.setdefault(competition, {})
                self.clubs_portraits[competition].setdefault(season, {})
                self.clubs_portraits[competition][season].setdefault("clubs_info", [])
                                
                for url in club_urls:   
                    if url not in urls:
                        club_portrait = self.browser.get_club_portrait(url)
                        self.clubs_portraits[competition][season]["clubs_info"].append(club_portrait)
                    else:
                        print(f"{url} found in repository.")

                save_to_json(self.clubs_portraits, "clubs_portraits.json")
        # 3 walkthrough all urls and add non-existing ones, if overwrite=True just add
        # 31 non-existing ones scrape and load data
        # 4 write data back to file
        return self.clubs_portraits

if __name__ == '__main__': 
    frc = FootballRepositoryController()

    start_time = time.time()
    frc.scrape_and_save_club_details("2024", "bundesliga", False)
    frc.scrape_and_save_club_details("2023", "bundesliga", False)
    frc.scrape_and_save_club_details("2022", "bundesliga", False)
    frc.scrape_and_save_club_details("2023", "2-bundesliga", False)
    frc.scrape_and_save_club_details("2022", "2-bundesliga", False)
    frc.scrape_and_save_club_details("2021", "2-bundesliga", False)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print("Elapsed time: ", round(elapsed_time,2))
    #frc.crawl_and_save_clubs_for_bl()
    # print(frc.scrape_and_save_club_infos("2024", "bundesliga", False))
    # print(frc.scrape_and_save_club_infos("2023", "bundesliga", False))
    # print(frc.scrape_and_save_club_infos("2022", "2-bundesliga", False))
    # print(frc.scrape_and_save_club_infos("2024", "2-bundesliga", False))
    # print(frc.scrape_and_save_club_infos("2023", "2-bundesliga", False))
    # print(frc.scrape_and_save_club_infos("2022", "bundesliga", False))




