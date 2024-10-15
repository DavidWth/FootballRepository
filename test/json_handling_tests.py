import unittest
import json
from import_export_json import save_to_json

class JSONUnitTests(unittest.TestCase):
    def setUp(self):
        self.match = {'home_team': 'VfB Stuttgart', 'away_team': 'VfL Bochum', 'half_time_score': '2:0', 'full_time_score': '5:0', 'date': 'Sa, 19.08.2023', 'venue': 'MHP-Arena (Stuttgart)', 'attendance': 53000, 'local_time': '15:30', 
'is_soldOut': False}    
        
        self.players_info = [
            {'id': 'arthur-5', 'name': 'Arthur', 'url': 'https://www.kicker.de/arthur-5/spieler/bundesliga/2023-24/bayer-04-leverkusen'}, 
            {'id': 'jeremie-frimpong', 'name': 'Frimpong Jeremie', 'url': 'https://www.kicker.de/jeremie-frimpong/spieler/bundesliga/2023-24/bayer-04-leverkusen'}, 
            {'id': 'alejandro-grimaldo', 'name': 'Grimaldo Alejandro', 'url': 'https://www.kicker.de/alejandro-grimaldo/spieler/bundesliga/2023-24/bayer-04-leverkusen'}, 
            {'id': 'piero-hincapie', 'name': 'Hincapie Piero', 'url': 'https://www.kicker.de/piero-hincapie/spieler/bundesliga/2023-24/bayer-04-leverkusen'}, 
            {'id': 'odilon-kossounou', 'name': 'Kossounou Odilon', 'url': 'https://www.kicker.de/odilon-kossounou/spieler/bundesliga/2023-24/bayer-04-leverkusen'}, 
            {'id': 'josip-stanisic', 'name': 'Stanisic Josip', 'url': 'https://www.kicker.de/josip-stanisic/spieler/bundesliga/2023-24/bayer-04-leverkusen'}, 
            {'id': 'jonathan-tah', 'name': 'Tah Jonathan', 'url': 'https://www.kicker.de/jonathan-tah/spieler/bundesliga/2023-24/bayer-04-leverkusen'}, 
            {'id': 'edmond-tapsoba', 'name': 'Tapsoba Edmond', 'url': 'https://www.kicker.de/edmond-tapsoba/spieler/bundesliga/2023-24/bayer-04-leverkusen'}, 
            {'id': 'nadiem-amiri', 'name': 'Amiri Nadiem', 'url': 'https://www.kicker.de/nadiem-amiri/spieler/bundesliga/2023-24/bayer-04-leverkusen'}, 
            {'id': 'robert-andrich', 'name': 'Andrich Robert', 'url': 'https://www.kicker.de/robert-andrich/spieler/bundesliga/2023-24/bayer-04-leverkusen'}, 
            {'id': 'jonas-hofmann', 'name': 'Hofmann Jonas', 'url': 'https://www.kicker.de/jonas-hofmann/spieler/bundesliga/2023-24/bayer-04-leverkusen'}, 
            {'id': 'noah-mbamba', 'name': 'Mbamba Noah', 'url': 'https://www.kicker.de/noah-mbamba/spieler/bundesliga/2023-24/bayer-04-leverkusen'},  
            {'id': 'gustavo-puerta', 'name': 'Puerta Gustavo', 'url': 'https://www.kicker.de/gustavo-puerta/spieler/bundesliga/2023-24/bayer-04-leverkusen'}, 
            {'id': 'florian-wirtz', 'name': 'Wirtz Florian', 'url': 'https://www.kicker.de/florian-wirtz/spieler/bundesliga/2023-24/bayer-04-leverkusen'}, 
            {'id': 'granit-xhaka', 'name': 'Xhaka Granit', 'url': 'https://www.kicker.de/granit-xhaka/spieler/bundesliga/2023-24/bayer-04-leverkusen'}, 
            {'id': 'amine-adli', 'name': 'Adli Amine', 'url': 'https://www.kicker.de/amine-adli/spieler/bundesliga/2023-24/bayer-04-leverkusen'}, 
            {'id': 'victor-boniface', 'name': 'Boniface Victor', 'url': 'https://www.kicker.de/victor-boniface/spieler/bundesliga/2023-24/bayer-04-leverkusen'}, 
            {'id': 'borja-iglesias', 'name': 'Borja Iglesias', 'url': 'https://www.kicker.de/borja-iglesias/spieler/bundesliga/2023-24/bayer-04-leverkusen'}, 
            {'id': 'adam-hlozek', 'name': 'Hlozek Adam', 'url': 'https://www.kicker.de/adam-hlozek/spieler/bundesliga/2023-24/bayer-04-leverkusen'}, 
            {'id': 'patrik-schick', 'name': 'Schick Patrik', 'url': 'https://www.kicker.de/patrik-schick/spieler/bundesliga/2023-24/bayer-04-leverkusen'},
        ]

    team_ratings = {'fc-bayern-muenchen': [['leroy-sane', -1],
  ['harry-kane', -1],
  ['mathys-tel', -1],
  ['sven-ulreich', 3.0],
  ['noussair-mazraoui', 3.5],
  ['dayot-upamecano', 3.0],
  ['min-jae-kim', 3.5],
  ['alphonso-davies', 2.0],
  ['leon-goretzka', 2.5],
  ['joshua-kimmich', 3.0],
  ['jamal-musiala', 2.5],
  ['kingsley-coman', 3.0],
  ['matthijs-de-ligt', -1],
  ['konrad-laimer', -1],
  ['thomas-mueller', -1],
  ['eric-maxim-choupo-moting', -1],
  ['tom-ritzy-huelsmann', -1],
  ['frans-kraetzig', -1],
  ['benjamin-pavard', -1],
  ['ryan-gravenberch', -1]],
 'werder-bremen': [['jiri-pavlenka', 4.0],
  ['amos-pieper', 4.0],
  ['milos-veljkovic', 4.0],
  ['marco-friedl-2', 4.5],
  ['mitchell-weiser', 3.5],
  ['senne-lynen', 4.0],
  ['anthony-jung', 4.0],
  ['jens-stage', 4.0],
  ['leonardo-bittencourt', 4.5],
  ['niclas-fuellkrug', 4.0],
  ['marvin-ducksch', 5.0],
  ['oliver-burke', 5.0],
  ['christian-gross-2', -1],
  ['romano-schmid', -1],
  ['dawid-kownacki', -1],
  ['leon-opitz', -1],
  ['michael-zetterer', -1],
  ['ilia-gruev-2', -1],
  ['nicolai-rapp', -1],
  ['justin-njinmah', -1]]}
    
    def tearDown(self) -> None:
        pass

    def test_save_dict_to_json(self):
        file_path = "match.json"
        save_to_json(self.match, file_path)

    def test_save_list_to_json(self):
        file_path = "players_info.json"
        save_to_json(self.players_info, file_path)

    def test_save_dict_to_json_in_one_line(self):
        file_path = "match_wo_line.json"
        save_to_json(self.team_ratings, file_path)

    def manual_testing(self):
        file_path = "bl_2324.json"
        with open(file_path, 'r', encoding='utf-8') as file:
            data = json.load(file)
        names = [goal["goal_scored_for"] for goal in data["goals"]]
        goals_x_team = {}
        for name in names:
            if name in goals_x_team:   
                goals_x_team[name] =+ 1
            else:
                goals_x_team[name] = 1 