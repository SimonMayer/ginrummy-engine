from services.database import execute_query, fetch_one

def create_meld(cursor, round_id, user_id, meld_type):
    query = """
    INSERT INTO `Melds` (`round_id`, `user_id`, `meld_type`)
    VALUES (%s, %s, %s)
    """
    cursor = execute_query(cursor, query, (round_id, user_id, meld_type))
    return cursor.lastrowid

def add_card_to_meld(cursor, meld_id, card_id, user_id):
    query = """
    INSERT INTO `Meld_Cards` (`meld_id`, `card_id`, `user_id`)
    VALUES (%s, %s, %s)
    """
    execute_query(cursor, query, (meld_id, card_id, user_id))
