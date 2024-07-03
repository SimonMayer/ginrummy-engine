from flask import request, jsonify, g
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import mysql.connector
from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database

def init_matches(app):
    @app.route('/matches', methods=['POST'])
    @jwt_required()
    def create_match():
        user_id = get_jwt_identity()  # Get the identity of the current user from the JWT
        config = load_database_config()
        connection = connect_to_database(config)
        cursor = connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO Matches (created_by, start_time, end_time) VALUES (%s, %s, NULL)",
                (user_id, datetime.now())
            )
            connection.commit()
            match_id = cursor.lastrowid
            return jsonify({"message": "Match created successfully", "match_id": match_id}), 201
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 400
        finally:
            cursor.close()
            connection.close()

    @app.route('/matches/<int:match_id>/participants', methods=['POST'])
    @jwt_required()
    def add_participants(match_id):
        user_ids = request.json.get('user_ids', [])
        if not user_ids:
            return jsonify({"error": "User IDs are required"}), 400

        config = load_database_config()
        connection = connect_to_database(config)
        cursor = connection.cursor()
        try:
            for user_id in user_ids:
                cursor.execute(
                    "INSERT INTO Match_Participants (match_id, user_id) VALUES (%s, %s)",
                    (match_id, user_id)
                )
            connection.commit()
            return jsonify({"message": "Participants added successfully"}), 201
        except mysql.connector.Error as err:
            connection.rollback()  # Roll back in case of error
            return jsonify({"error": str(err)}), 400
        finally:
            cursor.close()
            connection.close()

    @app.route('/matches', methods=['GET'])
    @jwt_required()
    def get_user_matches():
        user_id = get_jwt_identity()  # Get the identity of the current user from the JWT
        config = load_database_config()
        connection = connect_to_database(config)
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT match_id, created_by, start_time, end_time FROM Matches WHERE created_by = %s",
                (user_id,)
            )
            matches = cursor.fetchall()
            return jsonify(matches), 200
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 400
        finally:
            cursor.close()
            connection.close()
