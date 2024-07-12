from services.database import execute_query, fetch_one

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
    cursor.execute(query, (round_id,))
    return cursor.fetchall()

def remove_card(cursor, card_id, round_id):
    query = "DELETE FROM `Discard_Pile_Cards` WHERE `card_id` = %s AND `discard_pile_id` = (SELECT `discard_pile_id` FROM `Discard_Piles` WHERE `round_id` = %s)"
    execute_query(cursor, query, (card_id, round_id))

def clear_discard_pile(cursor, round_id):
    query = """
    DELETE FROM `Discard_Pile_Cards`
    WHERE `discard_pile_id` = (SELECT `discard_pile_id` FROM `Discard_Piles` WHERE `round_id` = %s)
    """
    execute_query(cursor, query, (round_id,))
