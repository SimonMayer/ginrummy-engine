from flask import jsonify, request
import mysql.connector
from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
from utils.decorators.jwt_custom_extensions import jwt_multi_source_auth_handler
import services.authentication as authentication_service
import services.database as database_service
import services.turns as turns_service
import services.hands as hands_service
import services.actions as actions_service
import services.cards as cards_service
import services.discard_pile as discard_pile_service
import services.stock_pile as stock_pile_service
import services.players as players_service

def init_match_action_routes(app):
    @app.route('/matches/<int:match_id>/actions/draw_from_stock_pile', methods=['POST'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def draw_from_stock_pile(match_id):
        user_id = authentication_service.get_user_id_from_jwt_identity()
        database_config = load_database_config()
        connection = connect_to_database(database_config)
        cursor = connection.cursor(buffered=True)

        try:
            database_service.start_transaction(connection)

            turn = turns_service.get_current_turn(cursor, match_id)
            validation_error = turns_service.validate_user_turn(turn, user_id)
            if validation_error:
                return jsonify(validation_error[0]), validation_error[1]

            turn_id = turn[0]
            round_id = turn[2]

            validation_error = actions_service.validate_no_draw_this_turn(cursor, turn_id)
            if validation_error:
                return jsonify(validation_error[0]), validation_error[1]

            card = stock_pile_service.get_top_card(cursor, round_id)
            if not card:
                return jsonify({"error": "Stock pile is empty"}), 400

            stock_pile_service.remove_card(cursor, card[0], round_id)

            hands_service.add_card_to_hand(cursor, card[0], user_id, round_id)

            actions_service.record_draw_from_stock_pile_action(cursor, turn_id, card[0])

            database_service.commit_transaction(connection)
            return jsonify({"message": "Card drawn successfully", "card_id": card[0]}), 200

        except mysql.connector.Error as err:
            return database_service.handle_error(connection, err, custom_messages={mysql.connector.errorcode.ER_DUP_ENTRY: "This card is already in a hand"})
        finally:
            database_service.close_resources(cursor, connection)

    @app.route('/matches/<int:match_id>/actions/draw_one_from_discard_pile', methods=['POST'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def draw_one_from_discard_pile(match_id):
        user_id = authentication_service.get_user_id_from_jwt_identity()
        database_config = load_database_config()
        connection = connect_to_database(database_config)
        cursor = connection.cursor(buffered=True)

        try:
            database_service.start_transaction(connection)

            turn = turns_service.get_current_turn(cursor, match_id)
            validation_error = turns_service.validate_user_turn(turn, user_id)
            if validation_error:
                return jsonify(validation_error[0]), validation_error[1]

            turn_id = turn[0]
            round_id = turn[2]

            validation_error = actions_service.validate_no_draw_this_turn(cursor, turn_id)
            if validation_error:
                return jsonify(validation_error[0]), validation_error[1]

            card = discard_pile_service.get_top_card(cursor, round_id)
            if not card:
                return jsonify({"error": "Discard pile is empty"}), 400

            discard_pile_service.remove_card(cursor, card[0], round_id)

            hands_service.add_card_to_hand(cursor, card[0], user_id, round_id)

            actions_service.record_draw_from_discard_pile_action(cursor, turn_id, card[0])

            database_service.commit_transaction(connection)
            return jsonify({"message": "Card drawn successfully from discard pile", "card_id": card[0]}), 200

        except mysql.connector.Error as err:
            return database_service.handle_error(connection, err, custom_messages={mysql.connector.errorcode.ER_DUP_ENTRY: "This card is already in a hand"})
        finally:
            database_service.close_resources(cursor, connection)

    @app.route('/matches/<int:match_id>/actions/draw_from_empty_stock_pile', methods=['POST'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def draw_from_empty_stock_pile(match_id):
        user_id = authentication_service.get_user_id_from_jwt_identity()
        database_config = load_database_config()
        connection = connect_to_database(database_config)
        cursor = connection.cursor(buffered=True)

        try:
            database_service.start_transaction(connection)

            turn = turns_service.get_current_turn(cursor, match_id)
            validation_error = turns_service.validate_user_turn(turn, user_id)
            if validation_error:
                return jsonify(validation_error[0]), validation_error[1]

            turn_id = turn[0]
            round_id = turn[2]

            validation_error = actions_service.validate_no_draw_this_turn(cursor, turn_id)
            if validation_error:
                return jsonify(validation_error[0]), validation_error[1]

            stock_card = stock_pile_service.get_top_card(cursor, round_id)
            if stock_card:
                return jsonify({"error": "Stock pile is not empty"}), 400

            discard_pile_cards = discard_pile_service.get_all_cards(cursor, round_id)
            if not discard_pile_cards:
                return jsonify({"error": "Discard pile is empty"}), 400

            stock_pile_service.add_cards(cursor, discard_pile_cards, round_id)
            discard_pile_service.clear_discard_pile(cursor, round_id)

            # Draw the top card from the newly filled stock pile
            card = stock_pile_service.get_top_card(cursor, round_id)
            if not card:
                return jsonify({"error": "Stock pile is still empty"}), 400

            stock_pile_service.remove_card(cursor, card[0], round_id)
            hands_service.add_card_to_hand(cursor, card[0], user_id, round_id)
            actions_service.record_draw_from_stock_pile_action(cursor, turn_id, card[0])

            database_service.commit_transaction(connection)
            return jsonify({"message": "Card drawn successfully", "card_id": card[0]}), 200

        except mysql.connector.Error as err:
            return database_service.handle_error(connection, err, custom_messages={mysql.connector.errorcode.ER_DUP_ENTRY: "This card is already in a hand"})
        finally:
            database_service.close_resources(cursor, connection)

    @app.route('/matches/<int:match_id>/actions/discard_card', methods=['POST'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def discard_card(match_id):
        user_id = authentication_service.get_user_id_from_jwt_identity()
        card_id = request.json.get('card_id')
        if not card_id:
            return jsonify({"error": "Card ID is required"}), 400

        database_config = load_database_config()
        connection = connect_to_database(database_config)
        cursor = connection.cursor(buffered=True)

        try:
            database_service.start_transaction(connection)

            turn = turns_service.get_current_turn(cursor, match_id)
            validation_error = turns_service.validate_user_turn(turn, user_id)
            if validation_error:
                return jsonify(validation_error[0]), validation_error[1]

            turn_id = turn[0]
            round_id = turn[2]

            validation_error = actions_service.validate_draw_this_turn(cursor, turn_id)
            if validation_error:
                return jsonify(validation_error[0]), validation_error[1]

            removal_error = hands_service.remove_card_from_hand(cursor, user_id, round_id, card_id)
            if removal_error:
                return removal_error

            discard_pile = discard_pile_service.get_discard_pile(cursor, round_id)
            if not discard_pile:
                return jsonify({"error": "Discard pile not found for the round"}), 400

            discard_pile_service.add_card_to_discard_pile(cursor, discard_pile[0], card_id)

            validation_error = cards_service.validate_card_exists(cursor, card_id)
            if validation_error:
                return validation_error

            actions_service.record_discard_action(cursor, turn_id, card_id)

            turns_service.end_turn(cursor, turn_id)

            players_list = players_service.get_all_players(cursor, match_id)
            if not players_list:
                return jsonify({"error": "No players found for the match"}), 400

            player_ids = [player[0] for player in players_list]
            current_player_index = player_ids.index(user_id)
            next_player_index = (current_player_index + 1) % len(player_ids)
            next_user_id = player_ids[next_player_index]

            next_rotation = turns_service.get_next_rotation_number(cursor, round_id, next_user_id)
            turns_service.start_turn(cursor, round_id, next_user_id, next_rotation)

            database_service.commit_transaction(connection)
            return jsonify({"message": "Card discarded successfully", "card_id": card_id}), 200

        except mysql.connector.Error as err:
            return database_service.handle_error(connection, err, custom_messages={})
        finally:
            database_service.close_resources(cursor, connection)
