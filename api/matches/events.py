from flask import Blueprint, Response
from flask_jwt_extended import jwt_required
import mysql.connector
import json
import time
from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
import services.database as database_service

events_blueprint = Blueprint('events', __name__)

@events_blueprint.route('/matches/<int:match_id>/events', methods=['GET'])
@jwt_required()
def stream_events(match_id):
    def event_stream():
        config = load_database_config()
        connection = connect_to_database(config)
        cursor = connection.cursor(buffered=True)

        last_action_id = None

        try:
            while True:
                query = """
                    SELECT `a`.`action_id`, `a`.`turn_id`, `a`.`action_type`, `a`.`public_details`
                    FROM `Actions` `a`
                    JOIN `Turns` `t` ON `a`.`turn_id` = `t`.`turn_id`
                    JOIN `Rounds` `r` ON `t`.`round_id` = `r`.`round_id`
                    WHERE `r`.`match_id` = %s
                """
                if last_action_id:
                    query += " AND `a`.`action_id` > %s ORDER BY `a`.`action_id` ASC"
                    cursor.execute(query, (match_id, last_action_id))
                else:
                    query += " ORDER BY `a`.`action_id` ASC"
                    cursor.execute(query, (match_id,))

                new_actions = cursor.fetchall()
                if new_actions:
                    last_action_id = new_actions[-1][0]
                    for action in new_actions:
                        action_data = {
                            'action_id': action[0],
                            'turn_id': action[1],
                            'action_type': action[2],
                            'public_details': action[3]
                        }
                        yield f'data: {json.dumps(action_data)}\n\n'

                connection.commit() # Ensure any pending transactions are committed
                time.sleep(0.5)

        except mysql.connector.Error as err:
            print(f"Error: {err}")

        finally:
            cursor.close()
            connection.close()

    return Response(event_stream(), mimetype='text/event-stream')
