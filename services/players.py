from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
from services.database import (
    execute_query,
    fetch_all,
    start_transaction,
    commit_transaction,
    rollback_transaction,
    close_resources,
)
import services.melds as melds_service

def get_all_players(cursor, match_id):
    query = "SELECT `user_id` FROM `Match_Players` WHERE `match_id` = %s ORDER BY `user_id`"
    players = fetch_all(cursor, query, (match_id,))
    return players
from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
from services.database import fetch_all, close_resources
import services.melds as melds_service

def get_players_data(round_id):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor()

    try:
        query = """
        SELECT `h`.`user_id`, MAX(`h`.`hand_id`) AS `hand_id`, COUNT(`hc`.`card_id`) AS `size`
        FROM `Hands` `h`
        JOIN `Hand_Cards` `hc` ON `h`.`hand_id` = `hc`.`hand_id`
        WHERE `h`.`round_id` = %s
        GROUP BY `h`.`user_id`
        """
        hands_data = fetch_all(cursor, query, (round_id,))
        players = []
        for user_id, hand_id, size in hands_data:
            melds = melds_service.get_user_melds(cursor, user_id, round_id)
            melds_list = []
            for meld in melds:
                meld_id = meld[0]
                meld_type = meld[1]
                cards = melds_service.get_cards_for_meld(cursor, round_id, meld_id)
                cards_list = [
                    {
                        "card_id": card[0],
                        "user_id": card[1],
                        "rank": card[2],
                        "suit": card[3],
                        "point_value": card[4]
                    }
                    for card in cards
                ]
                melds_list.append({
                    "meld_id": meld_id,
                    "meld_type": meld_type,
                    "cards": cards_list
                })
            players.append({
                "user_id": user_id,
                "hand": {
                    "hand_id": hand_id,
                    "size": size
                },
                "melds": melds_list
            })
        return players
    finally:
        close_resources(cursor, connection)

def add_players_to_match(match_id, user_ids):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor(buffered=True)
    try:
        start_transaction(connection)
        for user_id in user_ids:
            cursor = execute_query(
                cursor,
                "INSERT INTO `Match_Players` (`match_id`, `user_id`) VALUES (%s, %s)",
                (match_id, user_id)
            )
        commit_transaction(connection)
    except Exception as err:
        rollback_transaction(connection)
        raise err
    finally:
        close_resources(cursor, connection)

def get_players_for_match(match_id):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor()
    try:
        cursor = execute_query(
            cursor,
            """
            SELECT `Users`.`user_id`, `Users`.`username`
            FROM `Match_Players`
            JOIN `Users` ON `Match_Players`.`user_id` = `Users`.`user_id`
            WHERE `Match_Players`.`match_id` = %s
            """,
            (match_id,)
        )
        players = fetch_all(cursor, None, None)
        formatted_players = [
            {
                "user_id": player[0],
                "username": player[1]
            }
            for player in players
        ]
        return formatted_players
    finally:
        close_resources(cursor, connection)
