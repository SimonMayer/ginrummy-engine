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
        query = """
            SELECT DISTINCT `m`.`match_id`, `m`.`created_by`, `m`.`create_time`, `m`.`start_time`, `m`.`end_time`
            FROM `Matches` `m`
            LEFT JOIN `Match_Players` `mp` ON `m`.`match_id` = `mp`.`match_id`
            WHERE `mp`.`user_id` = %s
            OR `m`.`created_by` = %s
            """
        matches = fetch_all(cursor, query, (user_id, user_id))
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
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT `m`.`match_id`, `m`.`created_by`, `m`.`create_time`, `m`.`start_time`, `m`.`end_time`, `cr`.`round_id` AS `current_round_id`, `lr`.`latest_round_id`
            FROM `Matches` `m`
            LEFT JOIN `Rounds` `cr` ON `m`.`match_id` = `cr`.`match_id` AND `cr`.`end_time` IS NULL
            LEFT JOIN
                (
                    SELECT `match_id`, MAX(`round_id`) AS `latest_round_id`
                    FROM `Rounds`
                    GROUP BY `match_id`
                ) `lr` ON `m`.`match_id` = `lr`.`match_id`
            WHERE `m`.`match_id` = %s
            """
        match = fetch_one(cursor, query, (match_id,))
        if match:
            formatted_match = {
                "match_id": match['match_id'],
                "created_by": match['created_by'],
                "create_time": match['create_time'].isoformat() if match['create_time'] else None,
                "start_time": match['start_time'].isoformat() if match['start_time'] else None,
                "end_time": match['end_time'].isoformat() if match['end_time'] else None,
                "current_round_id": match['current_round_id'],
                "latest_round_id": match['latest_round_id'],
                "all_round_ids": get_match_round_ids_list(match_id)
            }
            return formatted_match
        else:
            return None
    finally:
        close_resources(cursor, connection)

def get_match_round_ids_list(match_id):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT `round_id` FROM `Rounds` WHERE `match_id` = %s"
        results = fetch_all(cursor, query, (match_id,))
        return [row['round_id'] for row in results]
    finally:
        close_resources(cursor, connection)

def start_match(match_id):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor(buffered=True)
    try:
        start_transaction(connection)
        match_query = "SELECT `start_time` FROM `Matches` WHERE `match_id` = %s"
        match = fetch_one(cursor, match_query, (match_id,))
        if not match:
            raise ValueError("Match not found")
        if match[0] is not None:
            raise ValueError("Match has already started")

        game_config = load_game_config()

        match_players_query = "SELECT `user_id` FROM `Match_Players` WHERE `match_id` = %s ORDER BY `user_id`"
        players = fetch_all(cursor, match_players_query, (match_id,))
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

        player_ids = [player[0] for player in players]
        rounds_service.create_round(match_id, player_ids)
    except Exception as err:
        rollback_transaction(connection)
        raise err
    finally:
        close_resources(cursor, connection)
