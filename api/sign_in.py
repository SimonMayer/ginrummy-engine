from flask import request, jsonify
from flask_jwt_extended import create_access_token
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
                return access_token
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
    finally:
        cursor.close()
        connection.close()
    return None

def init_auth_routes(app):
    """Initialize authentication routes for the app."""
    @app.route('/sign-in', methods=['POST'])
    def sign_in():
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        token = authenticate_user(username, password)
        if token:
            return jsonify({'token': token}), 200
        else:
            return jsonify({"msg": "Bad username or password"}), 401
