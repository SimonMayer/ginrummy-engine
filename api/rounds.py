from flask import request, jsonify
from flask_jwt_extended import jwt_required
import mysql.connector
from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database

def init_round_routes(app):
    @app.route('/rounds/<int:round_id>', methods=['GET'])
    @jwt_required()
    def get_round(round_id):
        config = load_database_config()
        connection = connect_to_database(config)
        cursor = connection.cursor()
        try:
            # Get the size of the stock pile
            cursor.execute(
                "SELECT COUNT(*) FROM Stock_Pile_Cards WHERE stock_pile_id = (SELECT stock_pile_id FROM Stock_Piles WHERE round_id = %s)",
                (round_id,)
            )
            stock_pile_size = cursor.fetchone()[0]

            # Get the sequenced list of cards in the discard pile
            cursor.execute(
                "SELECT c.card_id, c.rank, c.suit, c.point_value "
                "FROM Discard_Pile_Cards dpc "
                "JOIN Cards c ON dpc.card_id = c.card_id "
                "WHERE dpc.discard_pile_id = (SELECT discard_pile_id FROM Discard_Piles WHERE round_id = %s) "
                "ORDER BY dpc.sequence",
                (round_id,)
            )
            discard_pile = cursor.fetchall()
            discard_pile_list = [
                {
                    "card_id": card[0],
                    "rank": card[1],
                    "suit": card[2],
                    "point_value": card[3]
                }
                for card in discard_pile
            ]

            # Get the hands for each player and the cards they contain
            # Deprecation note: Showing cards in hands is deprecated and will be removed in future releases.
            cursor.execute(
                """
                SELECT h.hand_id, h.user_id, hc.card_id, c.rank, c.suit, c.point_value
                FROM Hands h
                JOIN Hand_Cards hc ON h.hand_id = hc.hand_id
                JOIN Cards c ON hc.card_id = c.card_id
                WHERE h.round_id = %s
                """,
                (round_id,)
            )
            hands_data = cursor.fetchall()
            hands = {}
            for hand_id, user_id, card_id, rank, suit, point_value in hands_data:
                if user_id not in hands:
                    hands[user_id] = {
                        "hand_id": hand_id,
                        "cards": [], # Deprecated: This property will be removed in future versions.

                        "size": 0  # Initialize size
                    }
                hands[user_id]["cards"].append({
                    "card_id": card_id,
                    "rank": rank,
                    "suit": suit,
                    "point_value": point_value
                })

            # Calculate the size of each hand
            for user_id in hands:
                hands[user_id]["size"] = len(hands[user_id]["cards"])

            result = {
                "round_id": round_id,
                "stock_pile_size": stock_pile_size,
                "discard_pile": discard_pile_list,
                "hands": hands
            }

            return jsonify(result), 200
        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 400
        finally:
            cursor.close()
            connection.close()
