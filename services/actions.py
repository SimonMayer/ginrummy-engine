from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
from services.database import fetch_all, close_resources, execute_query, fetch_one
from services.cards import get_card_details

def validate_no_draw_this_turn(cursor, turn_id):
    query = "SELECT `action_id` FROM `Actions` WHERE `turn_id` = %s AND `action_type` = 'draw' FOR UPDATE"
    if fetch_one(cursor, query, (turn_id,)):
        return {"error": "Drawing has already taken place this turn"}, 400
    return None

def validate_draw_this_turn(cursor, turn_id):
    query = "SELECT `action_id` FROM `Actions` WHERE `turn_id` = %s AND `action_type` = 'draw' FOR UPDATE"
    if not fetch_one(cursor, query, (turn_id,)):
        return {"error": "You must draw a card before you can perform this action"}, 400
    return None

def record_draw_from_stock_pile_action(cursor, turn_id, card_id):
    card_details = get_card_details(cursor, card_id)
    card_rank, card_suit = card_details

    query = """
    INSERT INTO `Actions` (`turn_id`, `action_type`, `full_details`, `public_details`)
    VALUES (%s, 'draw', CONCAT('Drew ', %s, ' ', %s, ' from stock pile'), 'Drew 1 card from stock pile')
    """
    execute_query(cursor, query, (turn_id, card_rank, card_suit))

def record_draw_from_discard_pile_action(cursor, turn_id, card_id):
    card_details = get_card_details(cursor, card_id)
    card_rank, card_suit = card_details

    query = """
    INSERT INTO `Actions` (`turn_id`, `action_type`, `full_details`, `public_details`)
    VALUES (%s, 'draw', CONCAT('Drew ', %s, ' ', %s, ' from discard pile'), CONCAT('Drew ', %s, ' ', %s, ' from discard pile'))
    """
    execute_query(cursor, query, (turn_id, card_rank, card_suit, card_rank, card_suit))

def record_discard_action(cursor, turn_id, card_id):
    card_details = get_card_details(cursor, card_id)
    card_rank, card_suit = card_details

    query = """
    INSERT INTO `Actions` (`turn_id`, `action_type`, `full_details`, `public_details`)
    VALUES (%s, 'discard', CONCAT('Discarded ', %s, ' ', %s), CONCAT('Discarded ', %s, ' ', %s))
    """
    execute_query(cursor, query, (turn_id, card_rank, card_suit, card_rank, card_suit))

def record_play_meld_action(cursor, turn_id, meld_description):
    query = """
    INSERT INTO `Actions` (`turn_id`, `action_type`, `full_details`, `public_details`)
    VALUES (%s, 'play_meld', %s, %s)
    """
    execute_query(cursor, query, (turn_id, f"Played a {meld_description}", f"Played a {meld_description}"))

def record_extend_meld_action(cursor, turn_id, meld_id, card_ids):
    card_details = [get_card_details(cursor, card_id) for card_id in card_ids]
    card_info = ", ".join([f"{rank} of {suit}" for rank, suit in card_details])
    query = """
    INSERT INTO `Actions` (`turn_id`, `action_type`, `full_details`, `public_details`)
    VALUES (%s, 'extend_meld', CONCAT('Extended meld ', %s, ' with cards: ', %s), CONCAT('Extended meld with cards: ', %s))
    """
    execute_query(cursor, query, (turn_id, meld_id, card_info, card_info))

def get_new_actions(match_id, latest_action_id=None):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor(buffered=True)

    try:
        query = """
            SELECT `a`.`action_id`, `a`.`turn_id`, `a`.`action_type`, `a`.`public_details`
            FROM `Actions` `a`
            JOIN `Turns` `t` ON `a`.`turn_id` = `t`.`turn_id`
            JOIN `Rounds` `r` ON `t`.`round_id` = `r`.`round_id`
            WHERE `r`.`match_id` = %s
        """
        params = [match_id]

        if latest_action_id is not None:
            query += " AND `a`.`action_id` > %s"
            params.append(latest_action_id)

        query += " ORDER BY `a`.`action_id` ASC"
        new_actions = fetch_all(cursor, query, params)
        return new_actions
    finally:
        close_resources(cursor, connection)
