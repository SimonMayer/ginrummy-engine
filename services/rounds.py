from datetime import datetime
import random
from utils.config_loader import load_database_config, load_game_config
from utils.database_connector import connect_to_database
from services.database import (
    execute_query,
    fetch_one,
    start_transaction,
    commit_transaction,
    rollback_transaction,
    close_resources,
    handle_error,
)

def create_round(match_id, players):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor(buffered=True)
    try:
        start_transaction(connection)
        current_time = datetime.now()
        cursor = execute_query(
            cursor,
            "INSERT INTO `Rounds` (`match_id`, `start_time`) VALUES (%s, %s)",
            (match_id, current_time)
        )
        round_id = cursor.lastrowid

        cursor = execute_query(
            cursor,
            "INSERT INTO `Discard_Piles` (`round_id`) VALUES (%s)",
            (round_id,)
        )
        cursor = execute_query(
            cursor,
            "INSERT INTO `Stock_Piles` (`round_id`) VALUES (%s)",
            (round_id,)
        )
        stock_pile_id = cursor.lastrowid

        # todo load this from config
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
        cards = [{'rank': rank, 'suit': suit} for rank in ranks for suit in suits]
        random.shuffle(cards)

        game_config = load_game_config()
        points_by_rank = game_config['pointsByRank']

        for card in cards:
            point_value = points_by_rank.get(card['rank'], 0)
            cursor = execute_query(
                cursor,
                "INSERT INTO `Cards` (`rank`, `suit`, `point_value`) VALUES (%s, %s, %s)",
                (card['rank'], card['suit'], point_value)
            )
            card_id = cursor.lastrowid
            card['card_id'] = card_id

        hand_size = game_config['handSize']
        for player in players:
            user_id = player[0]
            cursor = execute_query(
                cursor,
                "INSERT INTO `Hands` (`round_id`, `user_id`) VALUES (%s, %s)",
                (round_id, user_id)
            )
            hand_id = cursor.lastrowid

            for sequence in range(hand_size):
                card = cards.pop(0)
                cursor = execute_query(
                    cursor,
                    "INSERT INTO `Hand_Cards` (`hand_id`, `card_id`, `sequence`) VALUES (%s, %s, %s)",
                    (hand_id, card['card_id'], sequence + 1)
                )

        for sequence, card in enumerate(cards, start=1):
            cursor = execute_query(
                cursor,
                "INSERT INTO `Stock_Pile_Cards` (`stock_pile_id`, `card_id`, `sequence`) VALUES (%s, %s, %s)",
                (stock_pile_id, card['card_id'], sequence)
            )

        first_player = random.choice(players)[0]
        cursor = execute_query(
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
