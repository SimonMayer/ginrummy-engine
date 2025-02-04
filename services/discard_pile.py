from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
from services.database import execute_query, fetch_one, fetch_all, close_resources

def get_discard_pile(cursor, round_id):
    query = "SELECT `discard_pile_id` FROM `Discard_Piles` WHERE `round_id` = %s FOR UPDATE"
    discard_pile = fetch_one(cursor, query, (round_id,))
    return discard_pile

def get_next_sequence(cursor, discard_pile_id):
    query = "SELECT COALESCE(MAX(`sequence`), 0) + 1 FROM `Discard_Pile_Cards` WHERE `discard_pile_id` = %s FOR UPDATE"
    next_sequence = fetch_one(cursor, query, (discard_pile_id,))
    return next_sequence[0]

def add_card_to_discard_pile(cursor, discard_pile_id, card_id):
    next_sequence = get_next_sequence(cursor, discard_pile_id)
    query = "INSERT INTO `Discard_Pile_Cards` (`discard_pile_id`, `card_id`, `sequence`) VALUES (%s, %s, %s)"
    execute_query(cursor, query, (discard_pile_id, card_id, next_sequence))

def get_top_card(cursor, round_id):
    query = """
    SELECT `card_id` FROM `Discard_Pile_Cards`
    WHERE `discard_pile_id` = (SELECT `discard_pile_id` FROM `Discard_Piles` WHERE `round_id` = %s)
    ORDER BY `sequence` DESC LIMIT 1 FOR UPDATE;
    """
    card = fetch_one(cursor, query, (round_id,))
    return card

def get_all_cards(cursor, round_id):
    query = """
    SELECT `card_id` FROM `Discard_Pile_Cards`
    WHERE `discard_pile_id` = (SELECT `discard_pile_id` FROM `Discard_Piles` WHERE `round_id` = %s)
    ORDER BY `sequence` DESC FOR UPDATE;
    """
    return fetch_all(cursor, query, (round_id,))

def get_cards_upwards_from(cursor, round_id, discard_pile_card_ids):
    # First query to find the minimum sequence of the provided card IDs
    query_min_sequence = """
    SELECT `dp`.`discard_pile_id`, `dpc`.`sequence` FROM `Discard_Pile_Cards` `dpc`
    INNER JOIN `Discard_Piles` `dp` ON `dpc`.`discard_pile_id` = `dp`.`discard_pile_id`
    WHERE `dp`.`round_id` = %s AND `dpc`.`card_id` IN ({})
    ORDER BY `dpc`.`sequence` ASC LIMIT 1
    """
    formatted_query_min_sequence = query_min_sequence.format(','.join(['%s'] * len(discard_pile_card_ids)))
    min_sequence_result = fetch_one(cursor, formatted_query_min_sequence, (round_id, *discard_pile_card_ids))

    if not min_sequence_result:
        return []

    discard_pile_id = min_sequence_result[0]
    min_sequence = min_sequence_result[1]

    # Second query to get all cards with sequence >= min_sequence
    query_cards = """
    SELECT `card_id` FROM `Discard_Pile_Cards`
    WHERE `discard_pile_id` = %s
    AND `sequence` >= %s
    ORDER BY `sequence` DESC FOR UPDATE;
    """
    return fetch_all(cursor, query_cards, (discard_pile_id, min_sequence))

def remove_card(cursor, card_id, round_id):
    query = "DELETE FROM `Discard_Pile_Cards` WHERE `card_id` = %s AND `discard_pile_id` = (SELECT `discard_pile_id` FROM `Discard_Piles` WHERE `round_id` = %s)"
    execute_query(cursor, query, (card_id, round_id))

def clear_discard_pile(cursor, round_id):
    query = """
    DELETE FROM `Discard_Pile_Cards`
    WHERE `discard_pile_id` = (SELECT `discard_pile_id` FROM `Discard_Piles` WHERE `round_id` = %s)
    """
    execute_query(cursor, query, (round_id,))

def get_discard_pile_list(round_id):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor(dictionary=True)

    try:
        query = "SELECT `c`.`card_id`, `c`.`rank`, `c`.`suit`, `c`.`point_value` FROM `Discard_Pile_Cards` `dpc` JOIN `Cards` `c` ON `dpc`.`card_id` = `c`.`card_id` WHERE `dpc`.`discard_pile_id` = (SELECT `discard_pile_id` FROM `Discard_Piles` WHERE `round_id` = %s) ORDER BY `dpc`.`sequence`"
        return fetch_all(cursor, query, (round_id,))
    finally:
        close_resources(cursor, connection)
