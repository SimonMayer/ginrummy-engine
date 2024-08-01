from flask import request, jsonify
import services.users as users_service
from utils.config_loader import load_settings_config

settings = load_settings_config()
search_maximum_result_count = settings['searchMaximumResultCount']

def init_user_routes(app):
    @app.route('/users/search', methods=['GET'])
    def search_users():
        term = request.args.get('term', '')
        limit = request.args.get('limit', 10, type=int)
        page = request.args.get('page', 1, type=int)

        if not term:
            return jsonify({"error": "Search term is required"}), 400

        if limit < 1:
            return jsonify({"error": "Limit must be at least 1"}), 400

        if limit > search_maximum_result_count:
            limit = search_maximum_result_count

        if page < 1:
            return jsonify({"error": "Page must be at least 1"}), 400

        offset = (page - 1) * limit

        try:
            users = users_service.search_usernames(term, limit, offset)
            return jsonify(users), 200
        except Exception as err:
            return jsonify({"error": str(err)}), 500
