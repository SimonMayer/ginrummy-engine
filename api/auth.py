from flask import request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token, create_refresh_token
from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
import mysql.connector
import bcrypt

def authenticate_user(username, password):
    """Authenticate user and return JWT if valid."""
    config = load_database_config()
    connection = connect_to_database(config)
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT user_id, password_hash FROM Users WHERE username = %s", (username,))
        user = cursor.fetchone()
        if user:
            user_id, password_hash = user
            if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
                access_token = create_access_token(identity=user_id)
                refresh_token = create_refresh_token(identity=user_id)
                return access_token, refresh_token, user_id
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        cursor.close()
        connection.close()
    return None, None, None

def init_auth_routes(app):
    """Initialize authentication routes for the app."""
    @app.route('/auth/sign-in', methods=['POST'])
    def sign_in():
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        access_token, refresh_token, user_id = authenticate_user(username, password)
        if access_token:
            return jsonify({'access_token': access_token, 'refresh_token': refresh_token, 'user_id': user_id}), 200
        else:
            return jsonify({"msg": "Bad username or password"}), 401

    @app.route('/auth/refresh', methods=['POST'])
    @jwt_required(refresh=True)
    def refresh():
        identity = get_jwt_identity()
        access_token = create_access_token(identity=identity)
        return jsonify(access_token=access_token), 200
