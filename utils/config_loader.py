import json
import os
import sys

def load_config(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "../config/", filename)

    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        sys.exit("Database configuration file not found.")
    except json.JSONDecodeError:
        sys.exit("Error decoding the configuration file.")

def load_database_config():
    return load_config("database.json")
