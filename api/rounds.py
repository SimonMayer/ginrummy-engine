from flask import request, jsonify
from utils.decorators.jwt_custom_extensions import jwt_multi_source_auth_handler
import services.authentication as authentication_service
import services.melds as melds_service
import services.rounds as rounds_service
import services.hands as hands_service
import services.turns as turns_service
import services.stock_pile as stock_pile_service
import services.discard_pile as discard_pile_service
import services.players as players_service

def init_round_routes(app):
    @app.route('/rounds/<int:round_id>/players', methods=['GET'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def get_round_players(round_id):
        try:
            players = players_service.get_players_data(round_id)
            return jsonify(players), 200
        except Exception as err:
            return jsonify({"error": str(err)}), 400

    @app.route('/rounds/<int:round_id>/stock_pile', methods=['GET'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def get_stock_pile(round_id):
        try:
            result = {
                "size": stock_pile_service.get_stock_pile_size(round_id),
            }

            return jsonify(result), 200
        except Exception as err:
            return jsonify({"error": str(err)}), 400

    @app.route('/rounds/<int:round_id>/discard_pile', methods=['GET'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def get_discard_pile(round_id):
        try:
            discard_pile = discard_pile_service.get_discard_pile_list(round_id)
            return jsonify(discard_pile), 200
        except Exception as err:
            return jsonify({"error": str(err)}), 400

    @app.route('/rounds/<int:round_id>/melds', methods=['GET'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def get_melds(round_id):
        try:
            melds = melds_service.get_melds_data_for_round(round_id)
            return jsonify(melds), 200
        except Exception as err:
            return jsonify({"error": str(err)}), 400

    @app.route('/rounds/<int:round_id>/current_turn', methods=['GET'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def get_current_turn(round_id):
        try:
            turn_details = turns_service.get_current_turn_details(round_id)
            return jsonify(turn_details), 200 if turn_details else 404
        except Exception as err:
            return jsonify({"error": str(err)}), 400
