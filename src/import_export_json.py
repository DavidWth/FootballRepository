
import json

def save_to_json(data, file_path):
    """
    Save data to a JSON file.

    :param data: List of dictionaries to save.
    :param file_path: Path to the JSON file.
    :param overwrite: Boolean flag indicating whether to overwrite the file or append to it.
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as file:
            json.dump(data, file, indent=2, separators=(',', ':'), ensure_ascii=False)
        print(f"Data successfully written to {file_path}")
    except IOError as e:
        print(f"An error occurred while writing to the file: {e}")

    