from flask import jsonify, request
from utils.decorators.jwt_custom_extensions import jwt_multi_source_auth_handler
import services.authentication as authentication_service
import services.hands as hands_service

def init_hand_routes(app):
    @app.route('/hands/<int:hand_id>', methods=['GET'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def get_hand(hand_id):
        user_id = authentication_service.get_user_id_from_jwt_identity()
        try:
            hand = hands_service.get_hand_object(hand_id)
            if not hand:
                return jsonify({"error": "Hand not found"}), 404

            if hand['user_id'] != user_id:
                return jsonify({"error": "Unauthorized access"}), 403

            return jsonify(hand), 200
        except Exception as err:
            return jsonify({"error": str(err)}), 500
