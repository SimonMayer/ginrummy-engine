from functools import wraps
from flask import request, jsonify
from flask_jwt_extended import decode_token, verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError, JWTExtendedException
import logging
import services.authentication as authentication_service

def jwt_multi_source_auth_handler(permission_type='rest', accept_query_param=False):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            token = request.args.get('token') if accept_query_param else None
            if token:
                try:
                    decoded_token = decode_token(token)
                    request.environ['HTTP_AUTHORIZATION'] = f'Bearer {token}'
                    logging.info('Bearer header set from token query parameter')
                except JWTExtendedException as e:
                    logging.error(f"Invalid token: {e}")
                    return jsonify({"msg": "Invalid token"}), 401
            else:
                try:
                    verify_jwt_in_request()
                except NoAuthorizationError:
                    logging.error("Missing token")
                    return jsonify({"msg": "Missing token"}), 401

            # Verify the JWT again to ensure the context is properly set up
            try:
                verify_jwt_in_request()
            except NoAuthorizationError:
                logging.error("Token verification failed")
                return jsonify({"msg": "Token verification failed"}), 401

            if not authentication_service.has_permission(permission_type):
                logging.error(f"Permission denied: {permission_type}")
                return jsonify({"msg": "Permission denied"}), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator
