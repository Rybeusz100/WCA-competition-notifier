from config import get_config
from comps import get_upcoming_comps, get_known_comps, write_comps, get_updated_known_comps
from notifications import send_notifications
    
def main():
    config = get_config()
    upcoming_comps = get_upcoming_comps(config['country'])
    known_comps = get_known_comps()
    known_comps = get_updated_known_comps(known_comps, upcoming_comps)
    send_notifications(known_comps, config['ntfy_topic'])
    write_comps(known_comps)

main()
