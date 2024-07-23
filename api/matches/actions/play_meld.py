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
    @app.route('/matches/<int:match_id>/actions/play_meld/<string:meld_type>', methods=['POST'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def play_meld(match_id, meld_type):
        user_id = authentication_service.get_user_id_from_jwt_identity()
        card_ids = request.json.get('card_ids')
        if not card_ids or not isinstance(card_ids, list):
            return jsonify({"error": "A list of card IDs is required"}), 400

        game_config = load_game_config()
        min_meld_size = game_config['minimumMeldSize']
        allow_melds_from_rotation = game_config['allowMeldsFromRotation']
        run_orders = game_config.get('runOrders', [])

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
            rotation_number = turn[3]

            if rotation_number < allow_melds_from_rotation:
                return jsonify({"error": f"Melds can only be played from rotation {allow_melds_from_rotation}"}), 400

            validation_error = actions_service.validate_draw_this_turn(cursor, turn_id)
            if validation_error:
                return jsonify(validation_error[0]), validation_error[1]

            hand_cards = hands_service.get_all_cards_in_hand(cursor, user_id, round_id)
            hand_card_ids = [card[0] for card in hand_cards]

            if not all(card_id in hand_card_ids for card_id in card_ids):
                return jsonify({"error": "All provided cards must be in the user's hand"}), 400

            if len(hand_card_ids) - len(card_ids) < 1:
                return jsonify({"error": "User must have at least one card in hand after playing the meld"}), 400

            card_details = [cards_service.get_card_details(cursor, card_id) for card_id in card_ids]
            card_ranks = [card[0] for card in card_details]
            card_suits = [card[1] for card in card_details]

            if len(card_ids) < min_meld_size:
                return jsonify({"error": f"A meld must contain at least {min_meld_size} cards"}), 400

            if meld_type == 'set':
                if len(set(card_ranks)) != 1:
                    return jsonify({"error": "All cards in a set must be of the same rank"}), 400
                meld_description = f"set of '{card_ranks[0]}'s ({', '.join([card[1] for card in card_details])})"
            elif meld_type == 'run':
                if len(set(card_suits)) != 1:
                    return jsonify({"error": "All cards in a run must be of the same suit"}), 400

                if not melds_service.is_valid_run(card_ranks, run_orders):
                    return jsonify({"error": "The cards do not form a valid run"}), 400

                meld_description = f"run of '{', '.join(card_ranks)}' in suit '{card_suits[0]}'"
            else:
                return jsonify({"error": "Invalid meld type"}), 400

            meld_id = melds_service.create_meld(cursor, round_id, user_id, meld_type)

            for card_id in card_ids:
                hands_service.remove_card_from_hand(cursor, user_id, round_id, card_id)
                melds_service.add_card_to_meld(cursor, meld_id, card_id, user_id)

            actions_service.record_play_meld_action(cursor, turn_id, user_id, meld_description, card_ids)

            database_service.commit_transaction(connection)
            return jsonify({"message": "Meld played successfully", "meld_id": meld_id}), 200

        except mysql.connector.Error as err:
            return database_service.handle_error(connection, err)
        finally:
            database_service.close_resources(cursor, connection)
