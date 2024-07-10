from services.database import execute_query, fetch_one

def get_top_card(cursor, round_id):
    query = """
    SELECT `card_id` FROM `Stock_Pile_Cards`
    WHERE `stock_pile_id` = (SELECT `stock_pile_id` FROM `Stock_Piles` WHERE `round_id` = %s)
    ORDER BY `sequence` DESC LIMIT 1 FOR UPDATE;
    """
    card = fetch_one(cursor, query, (round_id,))
    return card

def remove_card(cursor, card_id, round_id):
    query = "DELETE FROM `Stock_Pile_Cards` WHERE `card_id` = %s AND `stock_pile_id` = (SELECT `stock_pile_id` FROM `Stock_Piles` WHERE `round_id` = %s)"
    execute_query(cursor, query, (card_id, round_id))
