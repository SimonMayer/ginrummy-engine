from flask import request, jsonify
import mysql.connector
from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
from utils.decorators.jwt_custom_extensions import jwt_multi_source_auth_handler

def init_match_player_routes(app):
    @app.route('/matches/<int:match_id>/players', methods=['POST'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def add_players(match_id):
        user_ids = request.json.get('user_ids', [])
        if not user_ids:
            return jsonify({"error": "User IDs are required"}), 400

        database_config = load_database_config()
        connection = connect_to_database(database_config)
        cursor = connection.cursor()
        try:
            for user_id in user_ids:
                cursor.execute(
                    "INSERT INTO Match_Players (match_id, user_id) VALUES (%s, %s)",
                    (match_id, user_id)
                )
            connection.commit()
            return jsonify({"message": "Players added successfully"}), 201
        except mysql.connector.Error as err:
            connection.rollback()  # Roll back in case of error
            return jsonify({"error": str(err)}), 400
        finally:
            cursor.close()
            connection.close()

    @app.route('/matches/<int:match_id>/players', methods=['GET'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def get_match_players(match_id):
        database_config = load_database_config()
        connection = connect_to_database(database_config)
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT Users.user_id, Users.username FROM Match_Players "
                "JOIN Users ON Match_Players.user_id = Users.user_id "
                "WHERE Match_Players.match_id = %s",
                (match_id,)
            )
            players = cursor.fetchall()
            formatted_players = [
                {
                    "user_id": player[0],
                    "username": player[1]
                }
                for player in players
            ]
            return jsonify(formatted_players), 200
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 400
        finally:
            cursor.close()
            connection.close()
