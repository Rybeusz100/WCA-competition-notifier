import requests

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
