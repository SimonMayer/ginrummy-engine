import argparse
import json
import mysql.connector
from utils.config_saver import save_database_config
from mysql.connector import Error

def connect_to_data_server(host, user, password):
    try:
        db_config = {
            'host': host,
            'user': user,
            'password': password or ''
        }
        connection = mysql.connector.connect(**db_config)
        return connection
    except Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

# Function to create a database and tables
def create_database_and_tables(connection, database_name):
    if connection is not None:
        try:
            cursor = connection.cursor()
            # Create database and select it
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name};")
            cursor.execute(f"USE {database_name};")

            # SQL to create tables
            table_creations = [
                """
                CREATE TABLE IF NOT EXISTS `Users` (
                    `user_id` INT AUTO_INCREMENT PRIMARY KEY,
                    `username` VARCHAR(255) UNIQUE NOT NULL,
                    `password_hash` VARCHAR(255) NOT NULL
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS `Matches` (
                    `match_id` INT AUTO_INCREMENT PRIMARY KEY,
                    `created_by` INT NOT NULL,
                    `create_time` DATETIME NOT NULL,
                    `start_time` DATETIME,
                    `end_time` DATETIME,
                    FOREIGN KEY (`created_by`) REFERENCES `Users`(`user_id`)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS `Match_Players` (
                    `match_id` INT NOT NULL,
                    `user_id` INT NOT NULL,
                    PRIMARY KEY (`match_id`, `user_id`),
                    FOREIGN KEY (`match_id`) REFERENCES `Matches`(`match_id`),
                    FOREIGN KEY (`user_id`) REFERENCES `Users`(`user_id`)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS `Rounds` (
                    `round_id` INT AUTO_INCREMENT PRIMARY KEY,
                    `match_id` INT NOT NULL,
                    `start_time` DATETIME NOT NULL,
                    `end_time` DATETIME,
                    FOREIGN KEY (`match_id`) REFERENCES `Matches`(`match_id`)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS `Turns` (
                    `turn_id` INT AUTO_INCREMENT PRIMARY KEY,
                    `round_id` INT NOT NULL,
                    `user_id` INT NOT NULL,
                    `rotation_number` INT NOT NULL,
                    `start_time` DATETIME NOT NULL,
                    `end_time` DATETIME,
                    FOREIGN KEY (`round_id`) REFERENCES `Rounds`(`round_id`),
                    FOREIGN KEY (`user_id`) REFERENCES `Users`(`user_id`)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS `Actions` (
                    `action_id` INT AUTO_INCREMENT PRIMARY KEY,
                    `turn_id` INT NOT NULL,
                    `action_type` ENUM('draw', 'play_meld', 'discard') NOT NULL,
                    `details` VARCHAR(255),
                    FOREIGN KEY (`turn_id`) REFERENCES `Turns`(`turn_id`)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS `Cards` (
                    `card_id` INT AUTO_INCREMENT PRIMARY KEY,
                    `rank` VARCHAR(10) NOT NULL,
                    `suit` VARCHAR(10) NOT NULL,
                    `point_value` INT NOT NULL
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS `Hands` (
                    `hand_id` INT AUTO_INCREMENT PRIMARY KEY,
                    `round_id` INT NOT NULL,
                    `user_id` INT NOT NULL,
                    FOREIGN KEY (`round_id`) REFERENCES `Rounds`(`round_id`),
                    FOREIGN KEY (`user_id`) REFERENCES `Users`(`user_id`)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS `Hand_Cards` (
                    `hand_card_id` INT AUTO_INCREMENT PRIMARY KEY,
                    `hand_id` INT NOT NULL,
                    `card_id` INT NOT NULL,
                    `sequence` INT NOT NULL,
                    FOREIGN KEY (`hand_id`) REFERENCES `Hands`(`hand_id`),
                    FOREIGN KEY (`card_id`) REFERENCES `Cards`(`card_id`)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS `Stock_Piles` (
                    `stock_pile_id` INT AUTO_INCREMENT PRIMARY KEY,
                    `round_id` INT NOT NULL,
                    FOREIGN KEY (`round_id`) REFERENCES `Rounds`(`round_id`)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS `Stock_Pile_Cards` (
                    `stock_pile_card_id` INT AUTO_INCREMENT PRIMARY KEY,
                    `stock_pile_id` INT NOT NULL,
                    `card_id` INT NOT NULL,
                    `sequence` INT NOT NULL,
                    FOREIGN KEY (`stock_pile_id`) REFERENCES `Stock_Piles`(`stock_pile_id`),
                    FOREIGN KEY (`card_id`) REFERENCES `Cards`(`card_id`)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS `Discard_Piles` (
                    `discard_pile_id` INT AUTO_INCREMENT PRIMARY KEY,
                    `round_id` INT NOT NULL,
                    FOREIGN KEY (`round_id`) REFERENCES `Rounds`(`round_id`)
                );
                """,
                """
                CREATE TABLE IF NOT EXISTS `Discard_Pile_Cards` (
                    `discard_pile_card_id` INT AUTO_INCREMENT PRIMARY KEY,
                    `discard_pile_id` INT NOT NULL,
                    `card_id` INT NOT NULL,
                    `sequence` INT NOT NULL,
                    FOREIGN KEY (`discard_pile_id`) REFERENCES `Discard_Piles`(`discard_pile_id`),
                    FOREIGN KEY (`card_id`) REFERENCES `Cards`(`card_id`)
                );
                """,
            ]

            for query in table_creations:
                cursor.execute(query)

            connection.commit()
            print("Database and tables created successfully.")
        except Error as e:
            print(f"Error creating database/tables: {str(e)}")
        finally:
            cursor.close()
            connection.close()
    else:
        print("Failed to connect to MySQL server.")

def main(host, database_name, user, password=None):
    connection = connect_to_data_server(host, user, password)
    if connection:
        create_database_and_tables(connection, database_name)

    config_data = {
        'host': host,
        'user': user,
        'password': password or '',
        'database': database_name
    }

    save_database_config(config_data)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create MySQL database and tables for GinRummy game.')
    parser.add_argument('--host', type=str, default='localhost', help='Host where MySQL is running')
    parser.add_argument('--database', type=str, required=True, help='Name of the database to create and use')
    parser.add_argument('--user', type=str, required=True, help='MySQL username')
    parser.add_argument('--password', type=str, help='MySQL password (optional)')

    args = parser.parse_args()

    main(args.host, args.database, args.user, args.password)
