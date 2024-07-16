from flask import request, jsonify
from utils.decorators.jwt_custom_extensions import jwt_multi_source_auth_handler
import services.players as players_service

def init_match_player_routes(app):
    @app.route('/matches/<int:match_id>/players', methods=['POST'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def add_players(match_id):
        user_ids = request.json.get('user_ids', [])
        if not user_ids:
            return jsonify({"error": "User IDs are required"}), 400

        try:
            players_service.add_players_to_match(match_id, user_ids)
            return jsonify({"message": "Players added successfully"}), 201
        except Exception as err:
            return jsonify({"error": str(err)}), 400

    @app.route('/matches/<int:match_id>/players', methods=['GET'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def get_match_players(match_id):
        try:
            players = players_service.get_players_for_match(match_id)
            return jsonify(players), 200
        except Exception as err:
            return jsonify({"error": str(err)}), 400
