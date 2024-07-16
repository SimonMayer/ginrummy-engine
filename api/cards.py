from flask import jsonify, request
from utils.decorators.jwt_custom_extensions import jwt_multi_source_auth_handler
import services.cards as cards_service

def init_card_routes(app):
    @app.route('/cards/<int:card_id>', methods=['GET'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def get_card(card_id):
        try:
            card_details = cards_service.get_card_object(card_id)
            if not card_details:
                return jsonify({"error": "Card not found"}), 404

            return jsonify(card_details), 200
        except Exception as err:
            return jsonify({"error": str(err)}), 500
