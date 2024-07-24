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
import services.discard_pile as discard_pile_service
import services.melds as melds_service
import services.cards as cards_service

def init_route(app):
    @app.route('/matches/<int:match_id>/actions/draw_multiple_from_discard_pile', methods=['POST'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def draw_multiple_from_discard_pile(match_id):
        user_id = authentication_service.get_user_id_from_jwt_identity()
        data = request.json
        discard_pile_card_ids = data.get('discard_pile_card_ids')
        hand_card_ids = data.get('hand_card_ids', [])
        meld_id = data.get('meld_id')
        extend_meld = True if meld_id else False

        if not discard_pile_card_ids or not isinstance(discard_pile_card_ids, list) or len(discard_pile_card_ids) == 0:
            return jsonify({"error": "At least one discard pile card ID is required"}), 400

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

            validation_error = actions_service.validate_no_draw_this_turn(cursor, turn_id)
            if validation_error:
                return jsonify(validation_error[0]), validation_error[1]

            user_melds = melds_service.get_user_melds(cursor, user_id, round_id)
            if not user_melds:
                return jsonify({"error": "User must have played at least one meld this round to draw multiple cards"}), 400

            upper_discard_pile_cards = discard_pile_service.get_cards_upwards_from(cursor, round_id, discard_pile_card_ids)
            discard_pile_card_ids_set = {card[0] for card in upper_discard_pile_cards}

            if not all(card_id in discard_pile_card_ids_set for card_id in discard_pile_card_ids):
                return jsonify({"error": "All provided discard pile card IDs must be in the discard pile", "card_ids": list(discard_pile_card_ids_set)}), 400

            if len(discard_pile_card_ids) == 1 and discard_pile_card_ids[0] == upper_discard_pile_cards[0][0]:
                return jsonify({"error": "Cannot draw the top card alone from the discard pile"}), 400

            hand_cards = hands_service.get_all_cards_in_hand(cursor, user_id, round_id)
            hand_card_ids_set = {card[0] for card in hand_cards}

            if not all(card_id in hand_card_ids_set for card_id in hand_card_ids):
                return jsonify({"error": "All provided hand card IDs must be in the user's hand"}), 400

            # Combine cards from hand and discard pile
            combined_card_ids = discard_pile_card_ids + hand_card_ids
            combined_card_details = [cards_service.get_card_details(cursor, card_id) for card_id in combined_card_ids]
            combined_card_ranks = [card[0] for card in combined_card_details]
            combined_card_suits = [card[1] for card in combined_card_details]

            game_config = load_game_config()
            min_meld_size = game_config['minimumMeldSize']
            run_orders = game_config.get('runOrders', [])

            if extend_meld:
                meld_cards = melds_service.get_cards_for_meld(cursor, round_id, meld_id)
                if not meld_cards:
                    return jsonify({"error": "Meld not found"}), 400

                meld_type = melds_service.get_meld_type(cursor, meld_id)
                meld_card_details = [cards_service.get_card_details(cursor, card[0]) for card in meld_cards]
                meld_card_ranks = [card[0] for card in meld_card_details]

                if meld_type == 'run':
                    meld_card_suits = [card[1] for card in meld_card_details]

                    valid_cards = []
                    for card_id in combined_card_ids:
                        card_details = cards_service.get_card_details(cursor, card_id)
                        card_rank, card_suit, card_point_value = card_details
                        if card_suit != meld_card_suits[0]:
                            return jsonify({"error": "All cards in a run must be of the same suit"}), 400
                        valid_cards.append((card_id, card_rank))

                    meld_card_ranks.extend([card[1] for card in valid_cards])

                    if not melds_service.is_valid_run(meld_card_ranks, run_orders):
                        return jsonify({"error": "The cards do not form a valid run"}), 400

                elif meld_type == 'set':
                    valid_rank = meld_card_ranks[0]
                    for card_id in combined_card_ids:
                        card_details = cards_service.get_card_details(cursor, card_id)
                        card_rank, card_suit, card_point_value = card_details
                        if card_rank != valid_rank:
                            return jsonify({"error": "All cards in a set must be of the same rank"}), 400

            else:
                if len(combined_card_ids) < min_meld_size:
                    return jsonify({"error": f"A meld must contain at least {min_meld_size} cards"}), 400

                if len(set(combined_card_ranks)) == 1:
                    # All cards have the same rank (set)
                    meld_description = f"set of '{combined_card_ranks[0]}'s"
                    meld_type = 'set'
                elif len(set(combined_card_suits)) == 1 and melds_service.is_valid_run(combined_card_ranks, run_orders):
                    # All cards have the same suit and form a valid run
                    meld_description = f"run of '{', '.join(combined_card_ranks)}' in suit '{combined_card_suits[0]}'"
                    meld_type = 'run'
                else:
                    return jsonify({"error": "The cards do not form a valid run or set"}), 400

                # Create meld
                meld_id = melds_service.create_meld(cursor, round_id, user_id, meld_type)

            new_hand_card_ids = []
            # Process cards from discard pile
            for card in reversed(upper_discard_pile_cards):
                discard_pile_service.remove_card(cursor, card[0], round_id)
                if card[0] in discard_pile_card_ids:
                    melds_service.add_card_to_meld(cursor, meld_id, card[0], user_id)
                else:
                    hands_service.add_card_to_hand(cursor, card[0], user_id, round_id)
                    new_hand_card_ids.append(card[0])

            # Process cards from hand
            for card_id in hand_card_ids:
                hands_service.remove_card_from_hand(cursor, user_id, round_id, card_id)
                melds_service.add_card_to_meld(cursor, meld_id, card_id, user_id)

            # Record action
            count = len(upper_discard_pile_cards)
            bottom_card = upper_discard_pile_cards[-1]
            bottom_card_details = cards_service.get_card_details(cursor, bottom_card[0])
            actions_service.record_draw_multiple_from_discard_pile_action(cursor, turn_id, count, bottom_card_details)

            if extend_meld:
                actions_service.record_extend_meld_action(cursor, turn_id, user_id, meld_id, combined_card_ids)
            else:
                actions_service.record_play_meld_action(cursor, turn_id, user_id, meld_description, combined_card_ids)

            database_service.commit_transaction(connection)

            return jsonify({
                "message": f"{count} cards drawn, starting from {bottom_card_details[0]} of {bottom_card_details[1]}",
                "new_hand_card_ids": new_hand_card_ids
            }), 200

        except mysql.connector.Error as err:
            return database_service.handle_error(connection, err)
        finally:
            database_service.close_resources(cursor, connection)
