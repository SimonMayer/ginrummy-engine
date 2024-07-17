from services.database import execute_query, fetch_one, fetch_all

def is_valid_run(meld_card_ranks, run_orders):
    for order in run_orders:
        positions = sorted(order.index(rank) for rank in meld_card_ranks)
        # Check if the positions form a consecutive sequence or a wrapped sequence
        if all((positions[i] - positions[i - 1]) % len(order) == 1 for i in range(1, len(positions))):
            return True
    return False

def get_user_melds(cursor, user_id, round_id):
    query = """
    SELECT `meld_id`, `meld_type`
    FROM `Melds`
    WHERE `user_id` = %s AND `round_id` = %s
    """
    return fetch_all(cursor, query, (user_id, round_id))

def get_cards_for_meld(cursor, round_id, meld_id):
    query = """
    SELECT `mc`.`card_id`, `mc`.`user_id`, `c`.`rank`, `c`.`suit`, `c`.`point_value`
    FROM `Meld_Cards` `mc`
    INNER JOIN `Cards` `c` ON `mc`.`card_id` = `c`.`card_id`
    INNER JOIN `Melds` `m` ON `mc`.`meld_id` = `m`.`meld_id`
    WHERE `mc`.`meld_id` = %s AND `m`.`round_id` = %s
    """
    return fetch_all(cursor, query, (meld_id, round_id))

def get_meld_type(cursor, meld_id):
    query = "SELECT `meld_type` FROM `Melds` WHERE `meld_id` = %s"
    meld_type = fetch_one(cursor, query, (meld_id,))
    return meld_type[0]

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
