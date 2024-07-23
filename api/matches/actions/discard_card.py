from flask import jsonify, request
import mysql.connector
from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
from utils.decorators.jwt_custom_extensions import jwt_multi_source_auth_handler
import services.authentication as authentication_service
import services.database as database_service
import services.actions as actions_service
import services.discard_pile as discard_pile_service
import services.cards as cards_service
import services.hands as hands_service
import services.players as players_service
import services.rounds as rounds_service
import services.scores as scores_service
import services.turns as turns_service

def init_route(app):
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

            user_hand = hands_service.get_user_hand(round_id, user_id)

            removal_error = hands_service.remove_card_from_hand(cursor, user_id, round_id, card_id)
            if removal_error:
                return jsonify(removal_error[0]), removal_error[1]

            discard_pile = discard_pile_service.get_discard_pile(cursor, round_id)
            if not discard_pile:
                return jsonify({"error": "Discard pile not found for the round"}), 400

            discard_pile_service.add_card_to_discard_pile(cursor, discard_pile[0], card_id)

            validation_error = cards_service.validate_card_exists(cursor, card_id)
            if validation_error:
                return jsonify(validation_error[0]), validation_error[1]

            action_id = actions_service.record_discard_action(cursor, turn_id, card_id)
            turns_service.end_turn(cursor, turn_id)

            players_list = players_service.get_all_players(cursor, match_id)

            if len(user_hand) == 1: # last card discarded
                rounds_service.end_round(cursor, round_id)

                # Update scores for each player
                for player in players_list:
                    player_id = player[0]
                    if player_id != user_id:
                        remaining_cards = hands_service.get_user_hand(round_id, player_id)
                        score_change = -sum(card['point_value'] for card in remaining_cards)
                        scores_service.record_score_change(cursor, action_id, player_id, score_change)

                database_service.commit_transaction(connection)
                return jsonify({
                    "message": "Card discarded, round ended and scores updated successfully",
                    "card_id": card_id,
                    "round_ended": True
                }), 200

            player_ids = [player[0] for player in players_list]
            current_player_index = player_ids.index(user_id)
            next_player_index = (current_player_index + 1) % len(player_ids)
            next_user_id = player_ids[next_player_index]

            next_rotation = turns_service.get_next_rotation_number(cursor, round_id, next_user_id)
            turns_service.start_turn(cursor, round_id, next_user_id, next_rotation)

            database_service.commit_transaction(connection)
            return jsonify({
                "message": "Card discarded successfully",
                "card_id": card_id,
                "round_ended": False
            }), 200

        except mysql.connector.Error as err:
            return database_service.handle_error(connection, err, custom_messages={})
        finally:
            database_service.close_resources(cursor, connection)
