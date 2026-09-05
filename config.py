import json

CONFIG_FILE = 'config.json'

def read_config():
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)
