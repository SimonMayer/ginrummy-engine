from flask import jsonify, request
from flask_jwt_extended import jwt_required
import mysql.connector
from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database

def init_card_routes(app):
    @app.route('/cards/<int:card_id>', methods=['GET'])
    @jwt_required()
    def get_card(card_id):
        config = load_database_config()
        connection = connect_to_database(config)
        cursor = connection.cursor(buffered=True)

        try:
            # Retrieve the card details
            cursor.execute("SELECT `card_id`, `rank`, `suit`, `point_value` FROM `Cards` WHERE `card_id` = %s", (card_id,))
            card = cursor.fetchone()
            if not card:
                return jsonify({"error": "Card not found"}), 404

            card_details = {
                "card_id": card[0],
                "rank": card[1],
                "suit": card[2],
                "point_value": card[3]
            }

            return jsonify(card_details), 200

        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            connection.close()
