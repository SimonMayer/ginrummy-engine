from flask import jsonify
from services.database import execute_query, fetch_one

def get_next_sequence(cursor, user_id, round_id):
    query = """
    SELECT COALESCE(MAX(`sequence`), 0) + 1
    FROM `Hand_Cards` WHERE `hand_id` IN
    (SELECT `hand_id` FROM `Hands` WHERE `user_id` = %s AND `round_id` = %s) FOR UPDATE;
    """
    next_sequence = fetch_one(cursor, query, (user_id, round_id))
    return next_sequence[0]

def add_card_to_hand(cursor, card_id, user_id, round_id):
    next_sequence = get_next_sequence(cursor, user_id, round_id)
    query = """
    INSERT INTO `Hand_Cards` (`hand_id`, `card_id`, `sequence`)
    SELECT `hand_id`, %s, %s FROM `Hands`
    WHERE `user_id` = %s AND `round_id` = %s
    """
    execute_query(cursor, query, (card_id, next_sequence, user_id, round_id))

def get_card_from_hand(cursor, user_id, round_id, card_id):
    query = """
    SELECT `hc`.`hand_card_id`, `hc`.`sequence`
    FROM `Hand_Cards` `hc`
    INNER JOIN `Hands` `h` ON `hc`.`hand_id` = `h`.`hand_id`
    WHERE `h`.`user_id` = %s AND `h`.`round_id` = %s AND `hc`.`card_id` = %s
    FOR UPDATE;
    """
    return fetch_one(cursor, query, (user_id, round_id, card_id))

def remove_card_from_hand(cursor, user_id, round_id, card_id):
    hand_card = get_card_from_hand(cursor, user_id, round_id, card_id)
    if not hand_card:
        return jsonify({"error": "Card not found in user's hand"}), 400

    query = "DELETE FROM `Hand_Cards` WHERE `hand_card_id` = %s"
    execute_query(cursor, query, (hand_card[0],))
    return None
