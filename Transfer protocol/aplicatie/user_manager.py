import json
import os
from datetime import datetime

HISTORY_FILE = "keys_history.json"
ACTIVE_FILE = "active_keys.json"

def load_keys(file_path):
    if not os.path.exists(file_path):
        return {}
    with open(file_path, "r") as file:
        return json.load(file)

def save_to_file(file_path, keys):
    with open(file_path, "w") as file:
        json.dump(keys, file, indent=4)

def add_key_to_history(username, key):
    keys = load_keys(HISTORY_FILE)
    if username not in keys:
        keys[username] = []
    keys[username].append({
        "key": key,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })
    save_to_file(HISTORY_FILE, keys)

def get_keys(username):
    keys = load_keys(HISTORY_FILE)
    return keys.get(username, [])

def save_active_key(username, key):
    active_keys = load_keys(ACTIVE_FILE)
    active_keys[username] = key
    save_to_file(ACTIVE_FILE, active_keys)

def get_active_key(username):
    active_keys = load_keys(ACTIVE_FILE)
    return active_keys.get(username, None)

def get_all_users():
    active_keys = load_keys(ACTIVE_FILE)
    return list(active_keys.keys())