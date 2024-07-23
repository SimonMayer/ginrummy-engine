from flask_jwt_extended import get_jwt_identity, create_access_token, create_refresh_token
from utils.config_loader import load_database_config
from utils.database_connector import connect_to_database
import mysql.connector
from services.database import fetch_one, close_resources, handle_error
import bcrypt

def create_access_token_with_permissions(user_id, rest_access, sse_access):
    return create_access_token(identity={
        'user_id': user_id,
        'permissions': {
            'rest': rest_access,
            'sse': sse_access
        }
    })

def create_rest_access_token(user_id):
    return create_access_token_with_permissions(user_id, True, False)

def create_sse_access_token(user_id):
    return create_access_token_with_permissions(user_id, False, True)

def get_user_id_from_jwt_identity():
    identity = get_jwt_identity()
    return identity['user_id']

def has_permission(permission_type):
    identity = get_jwt_identity()
    permissions = identity.get('permissions', {})
    return permissions.get(permission_type, False)

def authenticate_user(username, password):
    database_config = load_database_config()
    connection = connect_to_database(database_config)
    cursor = connection.cursor(buffered=True)
    try:
        user = fetch_one(cursor, "SELECT user_id, password_hash FROM Users WHERE username = %s", (username,))
        if user:
            user_id, password_hash = user
            if bcrypt.checkpw(password.encode('utf-8'), password_hash.encode('utf-8')):
                rest_access_token = create_rest_access_token(user_id)
                sse_access_token = create_sse_access_token(user_id)
                refresh_token = create_refresh_token(identity={'user_id': user_id})
                return rest_access_token, sse_access_token, refresh_token, user_id
    except mysql.connector.Error as err:
        handle_error(connection, err)
    finally:
        close_resources(cursor, connection)
    return None, None, None
