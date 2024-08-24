import json
import os
import sys

_cached_database_config = None
_cached_game_config = None
_cached_settings_config = None

def load_config(filename):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, '../config/', filename)

    try:
        with open(config_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        sys.exit(f'Configuration file {filename} not found.')
    except json.JSONDecodeError:
        sys.exit(f'Error decoding the configuration file {filename}.')

def load_database_config():
    global _cached_database_config
    if _cached_database_config is None:
        _cached_database_config = load_config('database.json')
    return _cached_database_config

def load_game_config():
    global _cached_game_config
    if _cached_game_config is None:
        _cached_game_config = load_config('game.json')
    return _cached_game_config

def load_settings_config():
    global _cached_settings_config
    if _cached_settings_config is None:
        _cached_settings_config = load_config('settings.json')
    return _cached_settings_config
