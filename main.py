import json
from datetime import datetime
import requests

COMPS_FILE = 'comps.json'

def get_upcoming_comps(country: str):
    UPCOMING_COMPS_URL = 'https://www.worldcubeassociation.org/api/v0/competition_index'

    query_params = {
        'include_cancelled': 'false',
        'ongoing_and_future': datetime.now().strftime('%Y-%m-%d'),
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
    
def find_new_comps(known_comps: list[dict], upcoming_comps: list[dict]):
    known_ids = [comp['id'] for comp in known_comps]
    upcoming_ids = [comp['id'] for comp in upcoming_comps]
    new_ids = [id for id in upcoming_ids if id not in known_ids]
    return [comp for comp in upcoming_comps if comp['id'] in new_ids]

def write_comps(comps: list[dict]):
    with open(COMPS_FILE, 'w') as f:
        json.dump([
            {
                'id': comp['id'],
                'name': comp['name'],
                'registration_open': comp['registration_open'],
                'start_date': comp['start_date'],
                'end_date': comp['end_date'],
                'notification_sent': comp.get('notification_sent', False)
            } for comp in comps], f, indent=2)

def send_notifications(comps: list[dict], topic: str):
    for comp in comps:
        if comp.get('notification_sent'):
            continue
        response = requests.post(f'https://ntfy.sh/{topic}',
                      data=comp['name'],
                      headers={
                          'Title': f'Competition announced',
                          'Click': f'https://www.worldcubeassociation.org/competitions/{comp['id']}',
                          'Icon': 'https://upload.wikimedia.org/wikipedia/commons/e/ec/World_Cube_Association_Logo.png'
                      })
        if response.ok:
            comp['notification_sent'] = True
            print(f'Sent notification - {comp['name']}')
    
def main():
    with open('config.json', 'r') as f:
        config = json.load(f)

    upcoming_comps = get_upcoming_comps(config['country'])
    known_comps = get_known_comps()
    new_comps = find_new_comps(known_comps, upcoming_comps)
    print(f"Found {len(new_comps)} new comps")
    all_comps = known_comps + new_comps
    send_notifications(all_comps, config['ntfy_topic'])
    write_comps(all_comps)

main()
