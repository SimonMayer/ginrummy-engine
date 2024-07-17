import os
import importlib

def init_match_action_routes(app):
    current_dir = os.path.dirname(__file__)
    for filename in os.listdir(current_dir):
        if filename.endswith(".py") and filename != "__init__.py":
            module_name = f"api.matches.actions.{filename[:-3]}"
            module = importlib.import_module(module_name)
            if hasattr(module, 'init_route'):
                module.init_route(app)
