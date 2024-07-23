from datetime import datetime
import random
from utils.config_loader import load_database_config, load_game_config
from utils.database_connector import connect_to_database
import mysql.connector
from services.database import (
    execute_query,
    fetch_one,
    start_transaction,
    commit_transaction,
    rollback_transaction,
    close_resources,
    handle_error,
)
import services.turns as turns_service

def get_current_round(match_id):
     database_config = load_database_config()
     connection = connect_to_database(database_config)
     cursor = connection.cursor()
     try:
         query = "SELECT `round_id` FROM `Rounds` WHERE `match_id` = %s AND `end_time` IS NULL"
         current_round = fetch_one(cursor, query, (match_id,))
         return current_round[0] if current_round else None
     finally:
         close_resources(cursor, connection)

def create_round(match_id, player_ids):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor(buffered=True)
    try:
        start_transaction(connection)

        first_player = turns_service.determine_first_player(match_id, player_ids, cursor)
        current_time = datetime.now()
        execute_query(
            cursor,
            "INSERT INTO `Rounds` (`match_id`, `start_time`) VALUES (%s, %s)",
            (match_id, current_time)
        )
        round_id = cursor.lastrowid

        execute_query(
            cursor,
            "INSERT INTO `Discard_Piles` (`round_id`) VALUES (%s)",
            (round_id,)
        )
        execute_query(
            cursor,
            "INSERT INTO `Stock_Piles` (`round_id`) VALUES (%s)",
            (round_id,)
        )
        stock_pile_id = cursor.lastrowid

        game_config = load_game_config()
        ranks = game_config['ranks']
        suits = game_config['suits']
        points_by_rank = game_config['pointsByRank']

        cards = [{'rank': rank, 'suit': suit} for rank in ranks for suit in suits]
        random.shuffle(cards)

        for card in cards:
            point_value = points_by_rank.get(card['rank'], 0)
            execute_query(
                cursor,
                "INSERT INTO `Cards` (`rank`, `suit`, `point_value`) VALUES (%s, %s, %s)",
                (card['rank'], card['suit'], point_value)
            )
            card_id = cursor.lastrowid
            card['card_id'] = card_id

        hand_size = game_config['handSize']
        for player_id in player_ids:
            user_id = player_id
            execute_query(
                cursor,
                "INSERT INTO `Hands` (`round_id`, `user_id`) VALUES (%s, %s)",
                (round_id, user_id)
            )
            hand_id = cursor.lastrowid

            for sequence in range(hand_size):
                card = cards.pop(0)
                execute_query(
                    cursor,
                    "INSERT INTO `Hand_Cards` (`hand_id`, `card_id`, `sequence`) VALUES (%s, %s, %s)",
                    (hand_id, card['card_id'], sequence + 1)
                )

        for sequence, card in enumerate(cards, start=1):
            execute_query(
                cursor,
                "INSERT INTO `Stock_Pile_Cards` (`stock_pile_id`, `card_id`, `sequence`) VALUES (%s, %s, %s)",
                (stock_pile_id, card['card_id'], sequence)
            )

        execute_query(
            cursor,
            "INSERT INTO `Turns` (`round_id`, `user_id`, `rotation_number`, `start_time`) VALUES (%s, %s, %s, %s)",
            (round_id, first_player, 1, current_time)
        )

        commit_transaction(connection)
        return round_id
    except mysql.connector.Error as err:
        rollback_transaction(connection)
        handle_error(connection, err)
        raise
    finally:
        close_resources(cursor, connection)

def end_round(cursor, round_id):
    query = "UPDATE `Rounds` SET `end_time` = NOW() WHERE `round_id` = %s"
    execute_query(cursor, query, (round_id,))
