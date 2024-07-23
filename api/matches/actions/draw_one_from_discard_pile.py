from flask import jsonify
import mysql.connector
from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
from utils.decorators.jwt_custom_extensions import jwt_multi_source_auth_handler
import services.authentication as authentication_service
import services.database as database_service
import services.turns as turns_service
import services.hands as hands_service
import services.actions as actions_service
import services.discard_pile as discard_pile_service

def init_route(app):
    @app.route('/matches/<int:match_id>/actions/draw_one_from_discard_pile', methods=['POST'])
    @jwt_multi_source_auth_handler(permission_type='rest')
    def draw_one_from_discard_pile(match_id):
        user_id = authentication_service.get_user_id_from_jwt_identity()
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

            card = discard_pile_service.get_top_card(cursor, round_id)
            if not card:
                return jsonify({"error": "Discard pile is empty"}), 400

            discard_pile_service.remove_card(cursor, card[0], round_id)

            hands_service.add_card_to_hand(cursor, card[0], user_id, round_id)

            actions_service.record_draw_one_from_discard_pile_action(cursor, turn_id, card[0])

            database_service.commit_transaction(connection)
            return jsonify({"message": "Card drawn successfully from discard pile", "card_id": card[0]}), 200

        except mysql.connector.Error as err:
            return database_service.handle_error(connection, err, custom_messages={mysql.connector.errorcode.ER_DUP_ENTRY: "This card is already in a hand"})
        finally:
            database_service.close_resources(cursor, connection)
