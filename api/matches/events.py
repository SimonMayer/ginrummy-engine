from flask import Blueprint, Response, request, stream_with_context
import json
import logging
import sys
import time
from utils.decorators.jwt_custom_extensions import jwt_multi_source_auth_handler
import services.actions as actions_service
import services.rounds as rounds_service
import services.turns as turns_service

events_blueprint = Blueprint('events', __name__)

@events_blueprint.route('/matches/<int:match_id>/events', methods=['GET'])
@jwt_multi_source_auth_handler(permission_type='sse', accept_query_param=True)
def stream_events(match_id):
    logging.info(f"Entering stream_events for match_id: {match_id}")
    latest_action_id = request.args.get('latest_action_id', default=None, type=int)

    if latest_action_id is None:
        latest_action_id = actions_service.get_latest_action_id(match_id)

    @stream_with_context
    def event_stream(latest_action_id):
        try:
            while True:
                new_actions = actions_service.get_new_actions(match_id, latest_action_id)
                if new_actions:
                    latest_action_id = int(new_actions[-1]['action_id'])
                    current_round_id = rounds_service.get_current_round(match_id)
                    current_turn = turns_service.get_current_turn(match_id)
                    current_turn_id = current_turn[0] if current_turn else None

                    for action in new_actions:
                        action_data = {
                            'action': {
                                'action_id': action['action_id'],
                                'action_type': action['action_type'],
                                'public_details': action['public_details']
                            },
                            'turn_id': action['turn_id'],
                            'round_id': action['round_id'],
                            'current_status': {
                                'round_id': current_round_id,
                                'turn_id': current_turn_id
                            }
                        }
                        yield f'data: {json.dumps(action_data)}\n\n'
                        sys.stdout.flush()
                time.sleep(0.5)

        except Exception as err:
            logging.error(f"Error streaming events: {err}")

    return Response(event_stream(latest_action_id), mimetype='text/event-stream')
