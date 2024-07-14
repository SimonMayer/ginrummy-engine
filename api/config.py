from flask import request, jsonify
from utils.config_loader import load_game_config
from utils.decorators.jwt_custom_extensions import jwt_multi_source_auth_handler

def init_config_routes(app):
    @app.route('/config/game', methods=['GET'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def get_game_config():
        try:
            game_config = load_game_config()
            return jsonify(game_config), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500
