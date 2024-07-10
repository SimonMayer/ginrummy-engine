import mysql.connector
from flask import jsonify

def execute_query(cursor, query, params):
    cursor.execute(query, params)
    return cursor

def fetch_one(cursor, query, params):
    cursor.execute(query, params)
    return cursor.fetchone()

def fetch_all(cursor, query, params):
    cursor.execute(query, params)
    return cursor.fetchall()

def start_transaction(connection):
    connection.start_transaction()

def commit_transaction(connection):
    connection.commit()

def rollback_transaction(connection):
    connection.rollback()

def close_resources(cursor, connection):
    cursor.close()
    connection.close()

def handle_error(connection, err, custom_messages=None):
    rollback_transaction(connection)
    if custom_messages and err.errno in custom_messages:
        return jsonify({"error": custom_messages[err.errno]}), 400
    return jsonify({"error": str(err)}), 500
