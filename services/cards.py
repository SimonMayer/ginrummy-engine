from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
from services.database import fetch_one, close_resources

def get_card_details(cursor, card_id):
    query = "SELECT `rank`, `suit` FROM `Cards` WHERE `card_id` = %s"
    card_details = fetch_one(cursor, query, (card_id,))
    return card_details

def validate_card_exists(cursor, card_id):
    card_details = get_card_details(cursor, card_id)
    if not card_details:
        return {"error": "Card details not found"}, 400
    return None

def get_card_object(card_id):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor(buffered=True)

    try:
        query = "SELECT `card_id`, `rank`, `suit`, `point_value` FROM `Cards` WHERE `card_id` = %s"
        card = fetch_one(cursor, query, (card_id,))
        if not card:
            return None

        card_details = {
            "card_id": card[0],
            "rank": card[1],
            "suit": card[2],
            "point_value": card[3]
        }

        return card_details
    except Exception as e:
        raise e
    finally:
        close_resources(cursor, connection)
