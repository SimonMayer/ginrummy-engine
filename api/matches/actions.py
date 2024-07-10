from flask import jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
import mysql.connector
from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database

def init_match_action_routes(app):
    @app.route('/matches/<int:match_id>/actions/draw_from_stock_pile', methods=['POST'])
    @jwt_required()
    def draw_from_stock_pile(match_id):
        user_id = get_jwt_identity()
        config = load_database_config()
        connection = connect_to_database(config)
        cursor = connection.cursor(buffered=True)

        try:
            # Start a transaction
            connection.start_transaction()

            # Determine the current turn
            cursor.execute("""
                SELECT `t`.`turn_id`, `t`.`user_id`, `t`.`round_id`
                FROM `Turns` `t`
                INNER JOIN `Rounds` `r` ON `t`.`round_id` = `r`.`round_id`
                WHERE `r`.`match_id` = %s AND `t`.`end_time` IS NULL
                FOR UPDATE;
                """,
                (match_id,)
            )
            turn = cursor.fetchone()
            if not turn:
                return jsonify({"error": "No active turn or match does not exist"}), 400
            if turn[1] != user_id:
                return jsonify({"error": "Not the authenticated user's turn"}), 403

            turn_id = turn[0]
            round_id = turn[2]

            # Check if an action of type 'draw' already exists for this turn
            cursor.execute("SELECT `action_id` FROM `Actions` WHERE `turn_id` = %s AND `action_type` = 'draw' FOR UPDATE", (turn_id,))
            if cursor.fetchone():
                return jsonify({"error": "Drawing has already taken place this turn"}), 400

            # Check if the stock pile is empty
            cursor.execute("SELECT `card_id` FROM `Stock_Pile_Cards` WHERE `stock_pile_id` = (SELECT `stock_pile_id` FROM `Stock_Piles` WHERE `round_id` = %s) ORDER BY `sequence` DESC LIMIT 1 FOR UPDATE", (round_id,))
            card = cursor.fetchone()
            if not card:
                return jsonify({"error": "Stock pile is empty"}), 400

            # Get the next sequence number for the user's hand
            cursor.execute("SELECT COALESCE(MAX(`sequence`), 0) + 1 FROM `Hand_Cards` WHERE `hand_id` IN (SELECT `hand_id` FROM `Hands` WHERE `user_id` = %s AND `round_id` = %s) FOR UPDATE", (user_id, round_id))
            next_sequence = cursor.fetchone()[0]

            # Delete the card from the stock pile
            cursor.execute("DELETE FROM `Stock_Pile_Cards` WHERE `card_id` = %s AND `stock_pile_id` = (SELECT `stock_pile_id` FROM `Stock_Piles` WHERE `round_id` = %s)", (card[0], round_id))

            # Add the card to the user's hand
            cursor.execute("INSERT INTO `Hand_Cards` (`hand_id`, `card_id`, `sequence`) SELECT `hand_id`, %s, %s FROM `Hands` WHERE `user_id` = %s AND `round_id` = %s", (card[0], next_sequence, user_id, round_id))

            # Create a new action of type 'draw'
            cursor.execute("INSERT INTO `Actions` (`turn_id`, `action_type`, `full_details`, `public_details`) VALUES (%s, 'draw', CONCAT('drew ', (SELECT `rank` FROM `Cards` WHERE `card_id` = %s), ' ', (SELECT `suit` FROM `Cards` WHERE `card_id` = %s), ' from stock pile'), 'drew 1 card from stock pile')", (turn_id, card[0], card[0]))

            connection.commit()
            return jsonify({"message": "Card drawn successfully", "card_id": card[0]}), 200

        except mysql.connector.Error as err:
            connection.rollback()
            if err.errno == mysql.connector.errorcode.ER_DUP_ENTRY:
                return jsonify({"error": "This card is already in a hand"}), 400
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            connection.close()

    @app.route('/matches/<int:match_id>/actions/discard_card', methods=['POST'])
    @jwt_required()
    def discard_card(match_id):
        user_id = get_jwt_identity()
        card_id = request.json.get('card_id')
        if not card_id:
            return jsonify({"error": "Card ID is required"}), 400

        config = load_database_config()
        connection = connect_to_database(config)
        cursor = connection.cursor(buffered=True)

        try:
            # Start a transaction
            connection.start_transaction()

            # Determine the current turn
            cursor.execute("""
                SELECT t.turn_id, t.user_id, t.round_id, t.rotation_number
                FROM Turns t
                INNER JOIN Rounds r ON t.round_id = r.round_id
                WHERE r.match_id = %s AND t.end_time IS NULL
                FOR UPDATE;
            """, (match_id,))
            turn = cursor.fetchone()
            if not turn:
                return jsonify({"error": "No active turn or match does not exist"}), 400
            if turn[1] != user_id:
                return jsonify({"error": "Not the authenticated user's turn"}), 403

            turn_id = turn[0]
            round_id = turn[2]

            # Check if an action of type 'draw' already exists for this turn
            cursor.execute("""
                SELECT action_id FROM Actions
                WHERE turn_id = %s AND action_type = 'draw'
                FOR UPDATE;
            """, (turn_id,))
            if not cursor.fetchone():
                return jsonify({"error": "You must draw a card before you can discard"}), 400

            # Check if the card is in the user's hand
            cursor.execute("""
                SELECT hc.hand_card_id, hc.sequence
                FROM Hand_Cards hc
                INNER JOIN Hands h ON hc.hand_id = h.hand_id
                WHERE h.user_id = %s AND h.round_id = %s AND hc.card_id = %s
                FOR UPDATE;
            """, (user_id, round_id, card_id))
            hand_card = cursor.fetchone()
            if not hand_card:
                return jsonify({"error": "Card not found in user's hand"}), 400

            # Remove the card from the user's hand
            cursor.execute("DELETE FROM Hand_Cards WHERE hand_card_id = %s", (hand_card[0],))

            # Get the discard pile id and the next sequence number for the discard pile
            cursor.execute("""
                SELECT discard_pile_id
                FROM Discard_Piles
                WHERE round_id = %s
                FOR UPDATE;
            """, (round_id,))
            discard_pile = cursor.fetchone()
            if not discard_pile:
                return jsonify({"error": "Discard pile not found for the round"}), 400

            cursor.execute("""
                SELECT COALESCE(MAX(sequence), 0) + 1
                FROM Discard_Pile_Cards
                WHERE discard_pile_id = %s
                FOR UPDATE;
            """, (discard_pile[0],))
            next_sequence = cursor.fetchone()[0]

            # Add the card to the discard pile
            cursor.execute("""
                INSERT INTO Discard_Pile_Cards (discard_pile_id, card_id, sequence)
                VALUES (%s, %s, %s);
            """, (discard_pile[0], card_id, next_sequence))

            # Get card rank and suit for action details
            cursor.execute("""
                SELECT `rank`, suit FROM Cards WHERE card_id = %s
            """, (card_id,))
            card_details = cursor.fetchone()
            if not card_details:
                return jsonify({"error": "Card details not found"}), 400
            card_rank = card_details[0]
            card_suit = card_details[1]

            # Create a new action of type 'discard'
            cursor.execute("""
                INSERT INTO Actions (turn_id, action_type, full_details, public_details)
                VALUES (%s, 'discard', CONCAT('Discarded ', %s, ' ', %s), CONCAT('Discarded ', %s, ' ', %s));
            """, (turn_id, card_rank, card_suit, card_rank, card_suit))

            # End the current turn
            cursor.execute("UPDATE Turns SET end_time = NOW() WHERE turn_id = %s", (turn_id,))

            # Get the players in the match
            cursor.execute("""
                SELECT user_id FROM Match_Players WHERE match_id = %s ORDER BY user_id;
            """, (match_id,))
            players = cursor.fetchall()
            if not players:
                return jsonify({"error": "No players found for the match"}), 400

            # Find the next player
            player_ids = [player[0] for player in players]
            current_player_index = player_ids.index(user_id)
            next_player_index = (current_player_index + 1) % len(player_ids)
            next_user_id = player_ids[next_player_index]

            # Determine the rotation number for the new turn
            cursor.execute("""
                SELECT rotation_number FROM Turns
                WHERE round_id = %s AND user_id = %s
                ORDER BY rotation_number DESC LIMIT 1;
            """, (round_id, next_user_id))
            last_turn = cursor.fetchone()
            if last_turn:
                next_rotation = last_turn[0] + 1
            else:
                next_rotation = 1

            # Create a new turn for the next player
            cursor.execute("""
                INSERT INTO Turns (round_id, user_id, rotation_number, start_time)
                VALUES (%s, %s, %s, NOW());
            """, (round_id, next_user_id, next_rotation))

            connection.commit()
            return jsonify({"message": "Card discarded successfully", "card_id": card_id}), 200

        except mysql.connector.Error as err:
            connection.rollback()
            return jsonify({"error": str(err)}), 500
        finally:
            cursor.close()
            connection.close()
