from flask import Blueprint, Response, request, stream_with_context
import mysql.connector
import json
import time
from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
from utils.decorators.jwt_custom_extensions import jwt_multi_source_auth_handler
import services.database as database_service
import services.authentication as authentication_service
import logging

events_blueprint = Blueprint('events', __name__)

@events_blueprint.route('/matches/<int:match_id>/events', methods=['GET'])
@jwt_multi_source_auth_handler(permission_type='sse', accept_query_param=True)
def stream_events(match_id):
    logging.info(f"Entering stream_events for match_id: {match_id}")
    latest_action_id = request.args.get('latest_action_id', default=None, type=int)

    @stream_with_context
    def event_stream(latest_action_id):
        database_config = load_database_config()
        connection = connect_to_database(database_config)
        cursor = connection.cursor(buffered=True)

        try:
            while True:
                query = """
                    SELECT `a`.`action_id`, `a`.`turn_id`, `a`.`action_type`, `a`.`public_details`
                    FROM `Actions` `a`
                    JOIN `Turns` `t` ON `a`.`turn_id` = `t`.`turn_id`
                    JOIN `Rounds` `r` ON `t`.`round_id` = `r`.`round_id`
                    WHERE `r`.`match_id` = %s
                """
                params = [match_id]

                if latest_action_id is not None:
                    query += " AND `a`.`action_id` > %s"
                    params.append(latest_action_id)

                query += " ORDER BY `a`.`action_id` ASC"
                cursor.execute(query, params)

                new_actions = cursor.fetchall()
                if new_actions:
                    latest_action_id = new_actions[-1][0]
                    for action in new_actions:
                        action_data = {
                            'action_id': action[0],
                            'turn_id': action[1],
                            'action_type': action[2],
                            'public_details': action[3]
                        }
                        yield f'data: {json.dumps(action_data)}\n\n'

                connection.commit()  # Ensure any pending transactions are committed
                time.sleep(0.5)

        except mysql.connector.Error as err:
            logging.error(f"Database error: {err}")

        finally:
            cursor.close()
            connection.close()

    return Response(event_stream(latest_action_id), mimetype='text/event-stream')
