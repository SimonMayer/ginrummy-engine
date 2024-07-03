import mysql.connector

def connect_to_database(config):
    """Establish a database connection using the provided configuration."""
    try:
        connection = mysql.connector.connect(
            host=config['host'],
            user=config['user'],
            password=config['password'],
            database=config['database']
        )
        return connection
    except mysql.connector.Error as err:
        sys.exit(f"Failed to connect to database: {err}")
