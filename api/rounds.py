from flask import request, jsonify
from flask_jwt_extended import jwt_required
import mysql.connector
from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
import services.authentication as authentication_service

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

            # Get the hand data for each player
            cursor.execute(
                """
                SELECT h.user_id, MAX(h.hand_id) AS hand_id, COUNT(hc.card_id) AS size
                FROM Hands h
                JOIN Hand_Cards hc ON h.hand_id = hc.hand_id
                WHERE h.round_id = %s
                GROUP BY h.user_id
                """,
                (round_id,)
            )
            hands_data = cursor.fetchall()
            hands = {}
            for user_id, hand_id, size in hands_data:
                 if user_id not in hands:
                    hands[user_id] = {
                        "hand_id": hand_id,
                        "user_id": user_id,
                        "size": size
                    }

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

    @app.route('/rounds/<int:round_id>/my_hand', methods=['GET'])
    @jwt_required()
    def get_my_hand(round_id):
        user_id = authentication_service.get_user_id_from_jwt_identity()

        config = load_database_config()
        connection = connect_to_database(config)
        cursor = connection.cursor()

        try:
            # Execute SQL query to get the card details from the user's hand
            cursor.execute(
                """
                SELECT c.card_id, c.rank, c.suit, c.point_value
                FROM Hands h
                JOIN Hand_Cards hc ON h.hand_id = hc.hand_id
                JOIN Cards c ON hc.card_id = c.card_id
                WHERE h.round_id = %s AND h.user_id = %s
                """,
                (round_id, user_id)
            )
            cards = cursor.fetchall()

            hand_details = [
                {
                    "card_id": card[0],
                    "rank": card[1],
                    "suit": card[2],
                    "point_value": card[3]
                } for card in cards
            ]

            return jsonify({"user_id": user_id, "round_id": round_id, "cards": hand_details}), 200

        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 400

        finally:
            cursor.close()
            connection.close()

    @app.route('/rounds/<int:round_id>/current_turn', methods=['GET'])
    @jwt_required()
    def get_current_turn(round_id):
        config = load_database_config()
        connection = connect_to_database(config)
        cursor = connection.cursor()

        try:
            # Query to find the current turn for the specified round and its actions
            cursor.execute("""
                SELECT t.turn_id, t.user_id, t.rotation_number, t.start_time,
                       a.action_id, a.action_type, a.public_details
                FROM Turns t
                LEFT JOIN Actions a ON t.turn_id = a.turn_id
                WHERE t.round_id = %s AND t.end_time IS NULL
                ORDER BY t.start_time DESC, a.action_id ASC
            """, (round_id,))
            result = cursor.fetchall()

            if result:
                # Extract turn details from the first row
                turn_details = {
                    "turn_id": result[0][0],
                    "user_id": result[0][1],
                    "rotation_number": result[0][2],
                    "start_time": result[0][3].strftime('%Y-%m-%d %H:%M:%S'),
                    "actions": []
                }

                # Append action details
                for row in result:
                    if row[4]:  # Ensure action_id is not None
                        turn_details["actions"].append({
                            "action_id": row[4],
                            "action_type": row[5],
                            "public_details": row[6]
                        })

                return jsonify(turn_details), 200
            else:
                return jsonify({"message": "No current turn found for this round"}), 404

        except mysql.connector.Error as err:
            return jsonify({"error": str(err)}), 400

        finally:
            cursor.close()
            connection.close()
