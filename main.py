import json
from datetime import datetime
import requests

CONFIG_FILE = 'config.json'
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

def get_updated_known_comps(known_comps: list[dict], upcoming_comps: list[dict]):
    updated_known = []
    for upcoming_comp in upcoming_comps:
        known_comp = next((comp for comp in known_comps if comp['id'] == upcoming_comp['id']), None)
        upcoming_comp['notifications'] = [] if known_comp is None else known_comp['notifications']
        if known_comp is None:
            upcoming_comp['notifications'].append('Competition announced')
        else:
            if known_comp['registration_open'] != upcoming_comp['registration_open']:
                upcoming_comp['notifications'].append('Registration date changed')
            if known_comp['start_date'] != upcoming_comp['start_date'] or known_comp['end_date'] != upcoming_comp['end_date']:
                upcoming_comp['notifications'].append('Competition date changed')
            
        updated_known.append(upcoming_comp)

    new_known_ids = [comp['id'] for comp in updated_known]
    updated_known += [comp for comp in known_comps if comp['id'] not in new_known_ids]
    return updated_known

def write_comps(comps: list[dict]):
    with open(COMPS_FILE, 'w') as f:
        json.dump([
            {
                'id': comp['id'],
                'name': comp['name'],
                'registration_open': comp['registration_open'],
                'start_date': comp['start_date'],
                'end_date': comp['end_date'],
                'notifications': comp.get('notifications')
            } for comp in comps], f, indent=2)

def send_notifications(comps: list[dict], topic: str):
    for comp in comps:
        notifications = comp.get('notifications')
        if notifications is None or len(notifications) == 0:
            continue

        for notification_reason in notifications:
            response = requests.post(f'https://ntfy.sh/{topic}',
                        data=comp['name'],
                        headers={
                            'Title': notification_reason,
                            'Click': f'https://www.worldcubeassociation.org/competitions/{comp['id']}',
                            'Icon': 'https://upload.wikimedia.org/wikipedia/commons/e/ec/World_Cube_Association_Logo.png'
                        })
            if response.ok:
                comp['notifications'] = [n for n in comp['notifications'] if n != notification_reason]
                print(f'Sent notification - {comp['name']}, {notification_reason}')
    
def main():
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)

    upcoming_comps = get_upcoming_comps(config['country'])
    known_comps = get_known_comps()
    known_comps = get_updated_known_comps(known_comps, upcoming_comps)
    send_notifications(known_comps, config['ntfy_topic'])
    write_comps(known_comps)

main()
