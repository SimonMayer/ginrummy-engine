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
    cursor = connection.cursor()

    try:
        query = "SELECT `c`.`card_id`, `c`.`rank`, `c`.`suit`, `c`.`point_value` FROM `Discard_Pile_Cards` `dpc` JOIN `Cards` `c` ON `dpc`.`card_id` = `c`.`card_id` WHERE `dpc`.`discard_pile_id` = (SELECT `discard_pile_id` FROM `Discard_Piles` WHERE `round_id` = %s) ORDER BY `dpc`.`sequence`"
        discard_pile = fetch_all(cursor, query, (round_id,))
        discard_pile_list = [
            {
                "card_id": card[0],
                "rank": card[1],
                "suit": card[2],
                "point_value": card[3]
            }
            for card in discard_pile
        ]
        return discard_pile_list
    finally:
        close_resources(cursor, connection)
