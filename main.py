import json
from datetime import datetime
import requests

COMPS_FILE = 'comps.json'

def get_upcoming_comps():
    UPCOMING_COMPS_URL = 'https://www.worldcubeassociation.org/api/v0/competition_index'

    with open('config.json', 'r') as f:
        config = json.load(f)

    country = config['country']
    today = datetime.now()

    query_params = {
        'include_cancelled': 'false',
        'ongoing_and_future': today.strftime('%Y-%m-%d'),
        'country_iso2': country
    }

    response = requests.get(UPCOMING_COMPS_URL, params=query_params)

    if response.status_code == 200:
        data = response.json()
        return data
    else:
        print(f"Error: {UPCOMING_COMPS_URL} responded with {response.status_code}")
        exit(1)

def get_known_comps():
    try:
        with open(COMPS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []
    
def find_new_comps(known_comps, upcoming_comps):
    known_ids = [comp['id'] for comp in known_comps]
    upcoming_ids = [comp['id'] for comp in upcoming_comps]
    new_ids = [id for id in upcoming_ids if id not in known_ids]
    return [comp for comp in upcoming_comps if comp['id'] in new_ids]

def write_comps(comps):
    with open(COMPS_FILE, 'w') as f:
        json.dump([
            {
                'id': comp['id'],
                'name': comp['name']
            } for comp in comps], f, indent=2)
    
def main():
    upcoming_comps = get_upcoming_comps()
    known_comps = get_known_comps()
    new_comps = find_new_comps(known_comps, upcoming_comps)
    print(f"Found {len(new_comps)} new comps")
    write_comps(known_comps + new_comps)

main()
