from datetime import datetime
import requests
import json
from notifications import create_notification

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

def read_known_comps():
    try:
        with open(COMPS_FILE, 'r') as f:
            return json.load(f)
    except:
        return []

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

def get_updated_known_comps(known_comps: list[dict], upcoming_comps: list[dict]):
    upcoming_ids = [comp['id'] for comp in upcoming_comps]
    updated_known = [comp for comp in known_comps if comp['id'] not in upcoming_ids]

    for upcoming_comp in upcoming_comps:
        known_comp = next((comp for comp in known_comps if comp['id'] == upcoming_comp['id']), None)
        upcoming_comp['notifications'] = [] if known_comp is None else known_comp['notifications']
        if known_comp is None:
            upcoming_comp['notifications'].append(create_notification('Competition announced'))
        else:
            if (old_reg_open := known_comp['registration_open']) != (new_reg_open := upcoming_comp['registration_open']):
                upcoming_comp['notifications'].append(create_notification(f'Registration changed from {old_reg_open} to {new_reg_open}'))
            if (old_start := known_comp['start_date']) != (new_start := upcoming_comp['start_date']) or (old_end := known_comp['end_date']) != (new_end := upcoming_comp['end_date']):
                upcoming_comp['notifications'].append(create_notification(f'Date changed from {old_start} - {old_end} to {new_start} - {new_end}'))
            
        updated_known.append(upcoming_comp)

    return updated_known
