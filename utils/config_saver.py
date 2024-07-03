import json
import os
import sys

def save_config(filename, config_data, config_identifier):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, "../config/", filename)

    os.makedirs(os.path.dirname(config_path), exist_ok=True)  # Ensure the directory exists
    with open(config_path, 'w') as file:
        json.dump(config_data, file, indent=4)
    print(f"{config_identifier} configuration saved successfully.")

def save_database_config(config_data):
    return save_config("database.json", config_data, "Database")
