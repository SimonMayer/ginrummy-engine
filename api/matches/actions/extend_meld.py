from flask import jsonify, request
import mysql.connector
from utils.config_loader import load_database_config, load_game_config
from utils.database_connector import connect_to_database
from utils.decorators.jwt_custom_extensions import jwt_multi_source_auth_handler
import services.authentication as authentication_service
import services.database as database_service
import services.turns as turns_service
import services.hands as hands_service
import services.actions as actions_service
import services.cards as cards_service
import services.melds as melds_service

def init_route(app):
    @app.route('/matches/<int:match_id>/actions/extend_meld/<int:meld_id>', methods=['POST'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def extend_meld(match_id, meld_id):
        user_id = authentication_service.get_user_id_from_jwt_identity()
        card_ids = request.json.get('card_ids')
        if not card_ids or not isinstance(card_ids, list) or len(card_ids) == 0:
            return jsonify({"error": "At least one card ID is required"}), 400

        database_config = load_database_config()
        connection = connect_to_database(database_config)
        cursor = connection.cursor(buffered=True)

        try:
            database_service.start_transaction(connection)

            turn = turns_service.get_current_turn(match_id)
            validation_error = turns_service.validate_user_turn(turn, user_id)
            if validation_error:
                return jsonify(validation_error[0]), validation_error[1]

            turn_id = turn[0]
            round_id = turn[2]

            validation_error = actions_service.validate_draw_this_turn(cursor, turn_id)
            if validation_error:
                return jsonify(validation_error[0]), validation_error[1]

            user_melds = melds_service.get_user_melds(cursor, user_id, round_id)
            if not user_melds:
                return jsonify({"error": "User must have played a meld this round to extend a meld"}), 400

            hand_cards = hands_service.get_all_cards_in_hand(cursor, user_id, round_id)
            hand_card_ids = [card[0] for card in hand_cards]

            if not all(card_id in hand_card_ids for card_id in card_ids):
                return jsonify({"error": "All provided cards must be in the user's hand"}), 400

            if len(hand_card_ids) - len(card_ids) < 1:
                return jsonify({"error": "User must have at least one card in hand after extending the meld"}), 400

            meld_cards = melds_service.get_cards_for_meld(cursor, round_id, meld_id)
            if not meld_cards:
                return jsonify({"error": "Meld not found"}), 400

            meld_type = melds_service.get_meld_type(cursor, meld_id)
            meld_card_details = [cards_service.get_card_details(cursor, card[0]) for card in meld_cards]
            meld_card_ranks = [card[0] for card in meld_card_details]

            if meld_type == 'run':
                meld_card_suits = [card[1] for card in meld_card_details]

                valid_cards = []
                for card_id in card_ids:
                    card_details = cards_service.get_card_details(cursor, card_id)
                    card_rank, card_suit, card_point_value = card_details
                    if card_suit != meld_card_suits[0]:
                        return jsonify({"error": "All cards in a run must be of the same suit"}), 400
                    valid_cards.append((card_id, card_rank))

                meld_card_ranks.extend([card[1] for card in valid_cards])
                run_orders = load_game_config().get('runOrders', [])

                if not melds_service.is_valid_run(meld_card_ranks, run_orders):
                    return jsonify({"error": "The cards do not form a valid run"}), 400

            elif meld_type == 'set':
                valid_rank = meld_card_ranks[0]
                for card_id in card_ids:
                    card_details = cards_service.get_card_details(cursor, card_id)
                    card_rank, card_suit, card_point_value = card_details
                    if card_rank != valid_rank:
                        return jsonify({"error": "All cards in a set must be of the same rank"}), 400

            for card_id in card_ids:
                hands_service.remove_card_from_hand(cursor, user_id, round_id, card_id)
                melds_service.add_card_to_meld(cursor, meld_id, card_id, user_id)

            actions_service.record_extend_meld_action(cursor, turn_id, user_id, meld_id, card_ids)

            database_service.commit_transaction(connection)
            return jsonify({"message": "Meld extended successfully"}), 200

        except mysql.connector.Error as err:
            return database_service.handle_error(connection, err)
        finally:
            database_service.close_resources(cursor, connection)
