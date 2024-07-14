import json
import mysql.connector
import bcrypt
import os
import sys
from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database

def create_user(connection, username, password):
    cursor = connection.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    try:
        cursor.execute(
            "INSERT INTO Users (username, password_hash) VALUES (%s, %s)",
            (username, hashed_password)
        )
        connection.commit()
        print("User created successfully.")
    except mysql.connector.Error as err:
        print(f"Failed to create user: {err}")
    finally:
        cursor.close()

def main():
    database_config = load_database_config()
    connection = connect_to_database(database_config)

    if len(sys.argv) != 3:
        print("Usage: python create_user.py <username> <password>")
        sys.exit(1)

    username = sys.argv[1]
    password = sys.argv[2]

    create_user(connection, username, password)
    connection.close()

if __name__ == "__main__":
    main()
