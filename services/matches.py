from datetime import datetime
from utils.config_loader import load_database_config, load_game_config
from utils.database_connector import connect_to_database
from services.database import (
    execute_query,
    fetch_one,
    fetch_all,
    start_transaction,
    commit_transaction,
    rollback_transaction,
    close_resources,
)

import services.rounds as rounds_service

def create_match(user_id):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor(buffered=True)
    try:
        start_transaction(connection)
        cursor = execute_query(
            cursor,
            "INSERT INTO `Matches` (`created_by`, `create_time`, `start_time`, `end_time`) VALUES (%s, %s, NULL, NULL)",
            (user_id, datetime.now())
        )
        match_id = cursor.lastrowid
        commit_transaction(connection)
        return match_id
    except Exception as err:
        rollback_transaction(connection)
        raise err
    finally:
        close_resources(cursor, connection)

def get_user_matches(user_id):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor()
    try:
        cursor = execute_query(
            cursor,
            """
            SELECT `m`.`match_id`, `m`.`created_by`, `m`.`create_time`, `m`.`start_time`, `m`.`end_time`
            FROM `Matches` `m`
            JOIN `Match_Players` `mp` ON `m`.`match_id` = `mp`.`match_id`
            WHERE `mp`.`user_id` = %s
            """,
            (user_id,)
        )
        matches = fetch_all(cursor, None, None)
        formatted_matches = [
            {
                "match_id": match[0],
                "created_by": match[1],
                "create_time": match[2].isoformat() if match[2] else None,
                "start_time": match[3].isoformat() if match[3] else None,
                "end_time": match[4].isoformat() if match[4] else None
            }
            for match in matches
        ]
        return formatted_matches
    finally:
        close_resources(cursor, connection)

def get_match(match_id):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor()
    try:
        cursor = execute_query(
            cursor,
            """
            SELECT `m`.`match_id`, `m`.`created_by`, `m`.`create_time`, `m`.`start_time`, `m`.`end_time`, `r`.`round_id` AS `current_round_id`
            FROM `Matches` `m`
            LEFT JOIN `Rounds` `r` ON `m`.`match_id` = `r`.`match_id` AND `r`.`end_time` IS NULL
            WHERE `m`.`match_id` = %s
            """,
            (match_id,)
        )
        match = fetch_one(cursor, None, None)
        if match:
            formatted_match = {
                "match_id": match[0],
                "created_by": match[1],
                "create_time": match[2].isoformat() if match[2] else None,
                "start_time": match[3].isoformat() if match[3] else None,
                "end_time": match[4].isoformat() if match[4] else None,
                "current_round_id": match[5]
            }
            return formatted_match
        else:
            return None
    finally:
        close_resources(cursor, connection)

def start_match(match_id):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor(buffered=True)
    try:
        start_transaction(connection)
        cursor = execute_query(
            cursor,
            "SELECT `start_time` FROM `Matches` WHERE `match_id` = %s",
            (match_id,)
        )
        match = fetch_one(cursor, None, None)
        if not match:
            raise ValueError("Match not found")
        if match[0] is not None:
            raise ValueError("Match has already started")

        game_config = load_game_config()

        cursor = execute_query(
            cursor,
            "SELECT `user_id` FROM `Match_Players` WHERE `match_id` = %s ORDER BY `user_id`",
            (match_id,)
        )
        players = fetch_all(cursor, None, None)
        player_count = len(players)

        min_players = game_config['players']['minimumAllowed']
        max_players = game_config['players']['maximumAllowed']
        if player_count < min_players or player_count > max_players:
            raise ValueError(f"Number of players must be between {min_players} and {max_players}")

        current_time = datetime.now()
        cursor = execute_query(
            cursor,
            "UPDATE `Matches` SET `start_time` = %s WHERE `match_id` = %s",
            (current_time, match_id)
        )
        commit_transaction(connection)

        rounds_service.create_round(match_id, players)
    except Exception as err:
        rollback_transaction(connection)
        raise err
    finally:
        close_resources(cursor, connection)
