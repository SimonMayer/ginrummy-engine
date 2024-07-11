from flask import request, jsonify
from flask_jwt_extended import jwt_required
from services.authentication import authenticate_user, create_rest_access_token, create_sse_access_token, get_user_id_from_jwt_identity

def init_auth_routes(app):
    """Initialize authentication routes for the app."""
    @app.route('/auth/sign-in', methods=['POST'])
    def sign_in():
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        rest_access_token, sse_access_token, refresh_token, user_id = authenticate_user(username, password)
        if user_id:
            return jsonify(
            {
                'rest_access_token': rest_access_token,
                'sse_access_token': sse_access_token,
                'refresh_token': refresh_token,
                'user_id': user_id
            }
            ), 200
        else:
            return jsonify({"msg": "Bad username or password"}), 401

    @app.route('/auth/refresh/rest', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh_rest():
        user_id = get_user_id_from_jwt_identity()
        access_token = create_rest_access_token(user_id)
        return jsonify(rest_access_token=access_token), 200

    @app.route('/auth/refresh/sse', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh_sse():
        user_id = get_user_id_from_jwt_identity()
        access_token = create_sse_access_token(user_id)
        return jsonify(sse_access_token=access_token), 200
