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
    @app.route('/rounds/<int:round_id>', methods=['GET'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def get_round(round_id):
        try:
            result = {
                "round_id": round_id,
                "stock_pile_size": stock_pile_service.get_stock_pile_size(round_id),
                "discard_pile": discard_pile_service.get_discard_pile_list(round_id),
                "players": players_service.get_players_data(round_id)
            }

            return jsonify(result), 200
        except Exception as err:
            return jsonify({"error": str(err)}), 400

    @app.route('/rounds/<int:round_id>/my_hand', methods=['GET'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def get_my_hand(round_id):
        user_id = authentication_service.get_user_id_from_jwt_identity()

        try:
            hand_details = hands_service.get_user_hand(round_id, user_id)
            return jsonify({"user_id": user_id, "round_id": round_id, "cards": hand_details}), 200
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
