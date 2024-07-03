from flask import request, jsonify, current_app
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
                "INSERT INTO Matches (created_by, create_time, start_time, end_time) VALUES (%s, %s, NULL, NULL)",
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

    @app.route('/matches/<int:match_id>/players', methods=['POST'])
    @jwt_required()
    def add_players(match_id):
        user_ids = request.json.get('user_ids', [])
        if not user_ids:
            return jsonify({"error": "User IDs are required"}), 400

        config = load_database_config()
        connection = connect_to_database(config)
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

    @app.route('/matches', methods=['GET'])
    @jwt_required()
    def get_user_matches():
        user_id = get_jwt_identity()  # Get the identity of the current user from the JWT
        config = load_database_config()
        connection = connect_to_database(config)
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT match_id, created_by, create_time, start_time, end_time FROM Matches WHERE created_by = %s",
                (user_id,)
            )
            matches = cursor.fetchall()
            formatted_matches = [
                {
                    "match_id": match[0],
                    "created_by": match[1],
                    "create_time": match[2].isoformat() if match[2] else None,
                    "start_time": match[3].isoformat() if match[3] else None,
                    "end_time": match[4].isoformat() if match[4] else None
                }
                for match in matches
            ]
            return jsonify(formatted_matches), 200
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 400
        finally:
            cursor.close()
            connection.close()

    @app.route('/matches/<int:match_id>', methods=['GET'])
    @jwt_required()
    def get_match(match_id):
        config = load_database_config()
        connection = connect_to_database(config)
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT match_id, created_by, create_time, start_time, end_time FROM Matches WHERE match_id = %s",
                (match_id,)
            )
            match = cursor.fetchone()
            if match:
                formatted_match = {
                    "match_id": match[0],
                    "created_by": match[1],
                    "create_time": match[2].isoformat() if match[2] else None,
                    "start_time": match[3].isoformat() if match[3] else None,
                    "end_time": match[4].isoformat() if match[4] else None
                }
                return jsonify(formatted_match), 200
            else:
                return jsonify({"error": "Match not found"}), 404
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 400
        finally:
            cursor.close()
            connection.close()

    @app.route('/matches/<int:match_id>/players', methods=['GET'])
    @jwt_required()
    def get_match_players(match_id):
        config = load_database_config()
        connection = connect_to_database(config)
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

    @app.route('/matches/<int:match_id>/start', methods=['POST'])
    @jwt_required()
    def start_match(match_id):
        config = load_database_config()
        connection = connect_to_database(config)
        cursor = connection.cursor()
        try:
            # Check if the match has already started
            cursor.execute(
                "SELECT start_time FROM Matches WHERE match_id = %s",
                (match_id,)
            )
            match = cursor.fetchone()
            if not match:
                return jsonify({"error": "Match not found"}), 404
            if match[0] is not None:
                return jsonify({"error": "Match has already started"}), 400

            # Get the number of players in the match
            cursor.execute(
                "SELECT COUNT(*) FROM Match_Players WHERE match_id = %s",
                (match_id,)
            )
            player_count = cursor.fetchone()[0]

            # Check if the number of players is within the allowed range
            min_players = current_app.config['MIN_PLAYERS']
            max_players = current_app.config['MAX_PLAYERS']
            if player_count < min_players or player_count > max_players:
                return jsonify({"error": f"Number of players must be between {min_players} and {max_players}"}), 400

            # Start the match
            cursor.execute(
                "UPDATE Matches SET start_time = %s WHERE match_id = %s",
                (datetime.now(), match_id)
            )
            connection.commit()
            return jsonify({"message": "Match started successfully"}), 200
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 400
        finally:
            cursor.close()
            connection.close()
