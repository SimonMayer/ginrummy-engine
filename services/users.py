from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
from services.database import fetch_all, close_resources

def search_usernames(term, limit=10, offset=0):
    if not isinstance(limit, int) or limit < 1:
        raise ValueError("Limit must be a positive integer")
    if not isinstance(offset, int) or offset < 0:
        raise ValueError("Offset must be a non-negative integer")

    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor(dictionary=True)

    try:
        query = """
        SELECT `user_id`, `username` FROM `Users`
        WHERE `username` LIKE %s LIMIT %s OFFSET %s
        """
        params = (f"%{term}%", limit, offset)
        return fetch_all(cursor, query, params)
    finally:
        close_resources(cursor, connection)
