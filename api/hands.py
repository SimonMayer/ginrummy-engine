from flask import request, jsonify
from flask_jwt_extended import jwt_required
import mysql.connector
from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database

def init_hand_routes(app):
    @app.route('/hands', methods=['GET'])
    @jwt_required()
    def get_hand():
        round_id = request.args.get('round_id')
        user_id = request.args.get('user_id')

        if not round_id or not user_id:
            return jsonify({"error": "round_id and user_id are required"}), 400

        config = load_database_config()
        connection = connect_to_database(config)
        cursor = connection.cursor()
        try:
            cursor.execute(
                "SELECT h.hand_id, hc.card_id, c.rank, c.suit, c.point_value "
                "FROM Hands h "
                "JOIN Hand_Cards hc ON h.hand_id = hc.hand_id "
                "JOIN Cards c ON hc.card_id = c.card_id "
                "WHERE h.round_id = %s AND h.user_id = %s",
                (round_id, user_id)
            )
            cards = cursor.fetchall()
            if not cards:
                return jsonify({"error": "Hand not found"}), 404

            hand = {
                "hand_id": cards[0][0],
                "cards": [
                    {
                        "card_id": card[1],
                        "rank": card[2],
                        "suit": card[3],
                        "point_value": card[4]
                    }
                    for card in cards
                ]
            }
            return jsonify(hand), 200
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 400
        finally:
            cursor.close()
            connection.close()
