from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
from services.database import execute_query, fetch_one, close_resources

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

def add_cards(cursor, cards, round_id):
    stock_pile_id_query = "SELECT `stock_pile_id` FROM `Stock_Piles` WHERE `round_id` = %s FOR UPDATE"
    stock_pile_id = fetch_one(cursor, stock_pile_id_query, (round_id,))[0]

    for sequence, card in enumerate(cards, start=1):
        query = """
        INSERT INTO `Stock_Pile_Cards` (`stock_pile_id`, `card_id`, `sequence`)
        VALUES (%s, %s, %s)
        """
        execute_query(cursor, query, (stock_pile_id, card[0], sequence))

def get_stock_pile_size(round_id):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor()

    try:
        query = "SELECT COUNT(*) FROM `Stock_Pile_Cards` WHERE `stock_pile_id` = (SELECT `stock_pile_id` FROM `Stock_Piles` WHERE `round_id` = %s)"
        stock_pile_size = fetch_one(cursor, query, (round_id,))[0]
        return stock_pile_size
    finally:
        close_resources(cursor, connection)
