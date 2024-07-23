from flask import request, jsonify
from datetime import datetime
from utils.decorators.jwt_custom_extensions import jwt_multi_source_auth_handler
import services.authentication as authentication_service
import services.matches as matches_service
import services.players as players_service
import services.rounds as rounds_service

def init_match_routes(app):
    @app.route('/matches', methods=['POST'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def create_match():
        user_id = authentication_service.get_user_id_from_jwt_identity()
        try:
            match_id = matches_service.create_match(user_id)
            return jsonify({"message": "Match created successfully", "match_id": match_id}), 201
        except Exception as err:
            return jsonify({"error": str(err)}), 400

    @app.route('/matches', methods=['GET'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def get_user_matches():
        user_id = authentication_service.get_user_id_from_jwt_identity()
        try:
            matches = matches_service.get_user_matches(user_id)
            return jsonify(matches), 200
        except Exception as err:
            return jsonify({"error": str(err)}), 400

    @app.route('/matches/<int:match_id>', methods=['GET'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def get_match(match_id):
        try:
            match = matches_service.get_match(match_id)
            if match:
                return jsonify(match), 200
            else:
                return jsonify({"error": "Match not found"}), 404
        except Exception as err:
            return jsonify({"error": str(err)}), 400

    @app.route('/matches/<int:match_id>/start', methods=['POST'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def start_match(match_id):
        user_id = authentication_service.get_user_id_from_jwt_identity()
        try:
            players = players_service.get_players_for_match(match_id)
            if user_id not in [player['user_id'] for player in players]:
                return jsonify({"error": "User is not a player in the match"}), 403

            matches_service.start_match(match_id)
            return jsonify({"message": "Match started successfully"}), 200
        except Exception as err:
            return jsonify({"error": str(err)}), 400

    @app.route('/matches/<int:match_id>/new_round', methods=['POST'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def start_new_round(match_id):
        user_id = authentication_service.get_user_id_from_jwt_identity()
        try:
            players = players_service.get_players_for_match(match_id)
            if user_id not in [player['user_id'] for player in players]:
                return jsonify({"error": "User is not a player in the match"}), 403

            current_round = rounds_service.get_current_round(match_id)
            if current_round is not None:
                return jsonify({"error": "Match already has an active round"}), 400

            player_ids = [player['user_id'] for player in players]
            round_id = rounds_service.create_round(match_id, player_ids)
            return jsonify({"message": "New round started successfully", "round_id": round_id}), 201
        except Exception as err:
            return jsonify({"error": str(err)}), 400
