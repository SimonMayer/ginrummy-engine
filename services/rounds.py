from datetime import datetime
import random
import mysql.connector
from flask import current_app
from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database

def create_round(match_id, players):
    config = load_database_config()
    connection = connect_to_database(config)
    cursor = connection.cursor()
    try:
        current_time = datetime.now()
        cursor.execute(
            "INSERT INTO Rounds (match_id, start_time) VALUES (%s, %s)",
            (match_id, current_time)
        )
        round_id = cursor.lastrowid

        # Create discard and stock piles
        cursor.execute(
            "INSERT INTO Discard_Piles (round_id) VALUES (%s)",
            (round_id,)
        )
        cursor.execute(
            "INSERT INTO Stock_Piles (round_id) VALUES (%s)",
            (round_id,)
        )
        stock_pile_id = cursor.lastrowid

        # Generate and shuffle cards
        ranks = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
        suits = ['Spades', 'Hearts', 'Clubs', 'Diamonds']
        cards = [{'rank': rank, 'suit': suit} for rank in ranks for suit in suits]
        random.shuffle(cards)

        points_by_rank = current_app.config['POINTS_BY_RANK']

        # Add cards to the Cards table and get their ids
        for card in cards:
            point_value = points_by_rank.get(card['rank'], 0)
            cursor.execute(
                "INSERT INTO Cards (`rank`, `suit`, `point_value`) VALUES (%s, %s, %s)",
                (card['rank'], card['suit'], point_value)
            )
            card_id = cursor.lastrowid
            card['card_id'] = card_id  # Store the card_id for later use

        # Create hands for each player and distribute cards
        hand_size = current_app.config['HAND_SIZE']
        for player in players:
            user_id = player[0]
            cursor.execute(
                "INSERT INTO Hands (round_id, user_id) VALUES (%s, %s)",
                (round_id, user_id)
            )
            hand_id = cursor.lastrowid

            for sequence in range(hand_size):
                card = cards.pop(0)
                cursor.execute(
                    "INSERT INTO Hand_Cards (hand_id, card_id, sequence) VALUES (%s, %s, %s)",
                    (hand_id, card['card_id'], sequence + 1)
                )

        # Add the remaining shuffled cards to the stock pile
        for sequence, card in enumerate(cards, start=1):
            cursor.execute(
                "INSERT INTO Stock_Pile_Cards (stock_pile_id, card_id, sequence) VALUES (%s, %s, %s)",
                (stock_pile_id, card['card_id'], sequence)
            )

        # Select a random player to start the first turn
        first_player = random.choice(players)[0]
        cursor.execute(
            "INSERT INTO Turns (round_id, user_id, turn_number, start_time) VALUES (%s, %s, %s, %s)",
            (round_id, first_player, 1, current_time)
        )

        connection.commit()
        return round_id
    except mysql.connector.Error as err:
        connection.rollback()
        raise
    finally:
        cursor.close()
        connection.close()
