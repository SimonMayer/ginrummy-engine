from flask import Blueprint, Response, request, stream_with_context
import json
import time
from utils.decorators.jwt_custom_extensions import jwt_multi_source_auth_handler
import services.actions as actions_service
import logging

events_blueprint = Blueprint('events', __name__)

@events_blueprint.route('/matches/<int:match_id>/events', methods=['GET'])
@jwt_multi_source_auth_handler(permission_type='sse', accept_query_param=True)
def stream_events(match_id):
    logging.info(f"Entering stream_events for match_id: {match_id}")
    latest_action_id = request.args.get('latest_action_id', default=None, type=int)

    @stream_with_context
    def event_stream(latest_action_id):
        try:
            while True:
                new_actions = actions_service.get_new_actions(match_id, latest_action_id)
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
                time.sleep(0.5)

        except Exception as err:
            logging.error(f"Error streaming events: {err}")

    return Response(event_stream(latest_action_id), mimetype='text/event-stream')
