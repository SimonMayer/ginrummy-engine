from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
from services.database import fetch_all, close_resources, execute_query, fetch_one
import services.cards as cards_service
import services.scores as scores_service

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
    card_details = cards_service.get_card_details(cursor, card_id)
    card_rank, card_suit, card_point_value = card_details

    query = """
    INSERT INTO `Actions` (`turn_id`, `action_type`, `full_details`, `public_details`)
    VALUES (%s, 'draw', CONCAT('Drew ', %s, ' ', %s, ' from stock pile'), 'Drew 1 card from stock pile')
    """
    execute_query(cursor, query, (turn_id, card_rank, card_suit))

def record_draw_one_from_discard_pile_action(cursor, turn_id, card_id):
    card_details = cards_service.get_card_details(cursor, card_id)
    card_rank, card_suit, card_point_value = card_details

    query = """
    INSERT INTO `Actions` (`turn_id`, `action_type`, `full_details`, `public_details`)
    VALUES (%s, 'draw', CONCAT('Drew ', %s, ' ', %s, ' from discard pile'), CONCAT('Drew ', %s, ' ', %s, ' from discard pile'))
    """
    execute_query(cursor, query, (turn_id, card_rank, card_suit, card_rank, card_suit))

def record_draw_multiple_from_discard_pile_action(cursor, turn_id, count, bottom_card_details):
    bottom_card_rank, bottom_card_suit, bottom_card_point_value = bottom_card_details
    full_details = f"{count} cards drawn, starting from {bottom_card_rank} of {bottom_card_suit}"
    public_details = full_details

    query = """
    INSERT INTO `Actions` (`turn_id`, `action_type`, `full_details`, `public_details`)
    VALUES (%s, 'draw', %s, %s)
    """
    execute_query(cursor, query, (turn_id, full_details, public_details))

def record_discard_action(cursor, turn_id, card_id):
    card_details = cards_service.get_card_details(cursor, card_id)
    card_rank, card_suit, card_point_value = card_details

    query = """
    INSERT INTO `Actions` (`turn_id`, `action_type`, `full_details`, `public_details`)
    VALUES (%s, 'discard', CONCAT('Discarded ', %s, ' ', %s), CONCAT('Discarded ', %s, ' ', %s))
    """
    execute_query(cursor, query, (turn_id, card_rank, card_suit, card_rank, card_suit))

def record_play_meld_action(cursor, turn_id, user_id, meld_description, card_ids):
    query = """
    INSERT INTO `Actions` (`turn_id`, `action_type`, `full_details`, `public_details`)
    VALUES (%s, 'play_meld', %s, %s)
    """
    cursor = execute_query(cursor, query, (turn_id, f"Played a {meld_description}", f"Played a {meld_description}"))
    action_id = cursor.lastrowid

    total_points = sum(cards_service.cards_service.get_card_details(cursor, card_id)[2] for card_id in card_ids)
    scores_service.record_score_change(cursor, action_id, user_id, total_points)

def record_extend_meld_action(cursor, turn_id, user_id, meld_id, card_ids):
    card_details = [cards_service.get_card_details(cursor, card_id) for card_id in card_ids]
    card_info = ", ".join([f"{rank} of {suit}" for rank, suit, point_value in card_details])
    query = """
    INSERT INTO `Actions` (`turn_id`, `action_type`, `full_details`, `public_details`)
    VALUES (%s, 'extend_meld', CONCAT('Extended meld ', %s, ' with cards: ', %s), CONCAT('Extended meld with cards: ', %s))
    """
    cursor = execute_query(cursor, query, (turn_id, meld_id, card_info, card_info))
    action_id = cursor.lastrowid

    total_points = sum(card[2] for card in card_details)
    scores_service.record_score_change(cursor, action_id, user_id, total_points)

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
