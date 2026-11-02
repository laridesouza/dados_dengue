import json
from pathlib import Path


def load_data(file_path):

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def list_json_files(folder):

    return sorted(Path(folder).glob("*.json"))