import json
import os

def save_to_json(data, file_path, flag='w'):
    """
    Save data to a JSON file.

    :param data: List of dictionaries to save.
    :param file_path: Path to the JSON file.
    :param overwrite: Boolean flag indicating whether to overwrite the file or append to it.
    """
    try:
        # Check if file exists
        # if not os.path.exists(file_path):
        #     raise FileNotFoundError(f"File '{file_path}' not found.")
        
        with open(file_path, flag, encoding='utf-8') as file:
            json.dump(data, file, indent=2, separators=(',', ':'), ensure_ascii=False)
        print(f"Data successfully written to {file_path}")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")

def load_from_json(file_path):
    data = None
    try:
        # Check if file exists
        # if not os.path.exists(file_path):
        #     raise FileNotFoundError(f"File '{file_path}' not found.")
        
        # Open and read the file
        with open(file_path, 'r') as file:
            data = json.load(file)  # Try to load the JSON data
            
        return data
    except FileNotFoundError as fnf_error:
        print(fnf_error)
    except json.JSONDecodeError as json_error:
        print(f"Error parsing JSON: {json_error}")


    return data
if __name__ == '__main__': 
    data = {
        "bundesliga":
        {
        "2024": 
            {
                "teams": 2,
                "clubs_info": [
                {
                  "name":"Bayern Munich",
                "url":"https://www.transfermarkt.com/fc-bayern-munchen/startseite/verein/27/saison_id/2023"
                },
                {
                "name":"Bayer 04 Leverkusen",
                "url":"https://www.transfermarkt.com/bayer-04-leverkusen/startseite/verein/15/saison_id/2023"
                },
            ] 
            }
        , 
        "2023": {
                "teams": 2,
                "clubs_info": [
                {
                  "name":"Bayern Munich",
                "url":"https://www.transfermarkt.com/fc-bayern-munchen/startseite/verein/27/saison_id/2023"
                },
                {
                "name":"Bayer 04 Leverkusen",
                "url":"https://www.transfermarkt.com/bayer-04-leverkusen/startseite/verein/15/saison_id/2023"
                },
            ] 
            }
        },

    }

    print(data["bundesliga"]["2024"])
    print(data["bundesliga"]["2023"])
    
    save_to_json(data, "test.json")