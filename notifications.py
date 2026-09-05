import requests
import uuid

def send_notifications(comps: list[dict], topic: str):
    for comp in comps:
        notifications = comp.get('notifications')
        if notifications is None or len(notifications) == 0:
            continue

        for notification in notifications:
            id, reason = notification['id'], notification['reason']
            response = requests.post(f'https://ntfy.sh/{topic}',
                        data=reason,
                        headers={
                            'Title': comp['name'].encode('utf-8'),
                            'Click': f'https://www.worldcubeassociation.org/competitions/{comp['id']}',
                        })
            if response.ok:
                comp['notifications'] = [n for n in comp['notifications'] if n['id'] != id]
                print(f'Sent notification - {comp['name']}, {reason}')

def create_notification(reason: str) -> dict:
    return {
        'id': str(uuid.uuid4()),
        'reason': reason,
    }
