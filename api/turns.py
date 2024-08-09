from flask import request, jsonify
from utils.decorators.jwt_custom_extensions import jwt_multi_source_auth_handler
import services.authentication as authentication_service
import services.turns as turns_service

def init_turn_routes(app):
    @app.route('/turns/<int:turn_id>', methods=['GET'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def get_turn(turn_id):
        user_id = authentication_service.get_user_id_from_jwt_identity()

        try:
            turn_details = turns_service.get_turn_object(turn_id, user_id)
            return jsonify(turn_details), 200 if turn_details else 404
        except Exception as err:
            return jsonify({"error": str(err)}), 400
