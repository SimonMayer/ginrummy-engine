from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
from services.database import close_resources, execute_query, fetch_one, fetch_all

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

def get_all_cards_in_hand(cursor, user_id, round_id):
    query = """
    SELECT `hc`.`card_id`, `c`.`rank`, `c`.`suit`
    FROM `Hand_Cards` `hc`
    INNER JOIN `Hands` `h` ON `hc`.`hand_id` = `h`.`hand_id`
    INNER JOIN `Cards` `c` ON `hc`.`card_id` = `c`.`card_id`
    WHERE `h`.`user_id` = %s AND `h`.`round_id` = %s
    """
    return fetch_all(cursor, query, (user_id, round_id))

def remove_card_from_hand(cursor, user_id, round_id, card_id):
    hand_card = get_card_from_hand(cursor, user_id, round_id, card_id)
    if not hand_card:
        return {"error": "Card not found in user's hand"}, 400

    query = "DELETE FROM `Hand_Cards` WHERE `hand_card_id` = %s"
    execute_query(cursor, query, (hand_card[0],))
    return None

def get_user_hand(round_id, user_id):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor()

    try:
        query = """
        SELECT `c`.`card_id`, `c`.`rank`, `c`.`suit`, `c`.`point_value`
        FROM `Hands` `h`
        JOIN `Hand_Cards` `hc` ON `h`.`hand_id` = `hc`.`hand_id`
        JOIN `Cards` `c` ON `hc`.`card_id` = `c`.`card_id`
        WHERE `h`.`round_id` = %s AND `h`.`user_id` = %s
        """
        cards = fetch_all(cursor, query, (round_id, user_id))
        hand_details = [
            {
                "card_id": card[0],
                "rank": card[1],
                "suit": card[2],
                "point_value": card[3]
            } for card in cards
        ]
        return hand_details
    finally:
        close_resources(cursor, connection)
