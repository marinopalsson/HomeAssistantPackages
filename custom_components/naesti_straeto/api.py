import requests
import json

BASE_URL = "https://data01.straeto.is/data/dyn-data/s"

def fetch_busstop_data(busstop_id):
    url = f"{BASE_URL}/{busstop_id}.json"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_stop_name(stop_id, file_path):
    with open(file_path, 'r') as f:
        stops_data = json.load(f)

    for stop in stops_data:
        if stop["stop_id"] == stop_id:
            return stop["stop_name"]
    
    return None