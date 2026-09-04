import json

CONFIG_FILE = 'config.json'

def get_config():
    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
    return config
