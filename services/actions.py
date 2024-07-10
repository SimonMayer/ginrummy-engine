from flask import jsonify
from services.database import execute_query, fetch_one
from services.cards import get_card_details

def validate_no_draw_this_turn(cursor, turn_id):
    query = "SELECT `action_id` FROM `Actions` WHERE `turn_id` = %s AND `action_type` = 'draw' FOR UPDATE"
    if fetch_one(cursor, query, (turn_id,)):
        return jsonify({"error": "Drawing has already taken place this turn"}), 400
    return None

def validate_draw_this_turn(cursor, turn_id):
    query = "SELECT `action_id` FROM `Actions` WHERE `turn_id` = %s AND `action_type` = 'draw' FOR UPDATE"
    if not fetch_one(cursor, query, (turn_id,)):
        return jsonify({"error": "You must draw a card before you can perform this action"}), 400
    return None

def record_draw_action(cursor, turn_id, card_id):
    query = """
    INSERT INTO `Actions` (`turn_id`, `action_type`, `full_details`, `public_details`)
    VALUES (%s, 'draw', CONCAT('drew ', (SELECT `rank` FROM `Cards` WHERE `card_id` = %s), ' ', (SELECT `suit` FROM `Cards` WHERE `card_id` = %s), ' from stock pile'), 'drew 1 card from stock pile')
    """
    execute_query(cursor, query, (turn_id, card_id, card_id))

def record_discard_action(cursor, turn_id, card_id):
    card_details = get_card_details(cursor, card_id)
    card_rank, card_suit = card_details

    query = """
    INSERT INTO `Actions` (`turn_id`, `action_type`, `full_details`, `public_details`)
    VALUES (%s, 'discard', CONCAT('Discarded ', %s, ' ', %s), CONCAT('Discarded ', %s, ' ', %s))
    """
    execute_query(cursor, query, (turn_id, card_rank, card_suit, card_rank, card_suit))
