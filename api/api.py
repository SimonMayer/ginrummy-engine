from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from api.auth import init_auth_routes
from api.cards import init_card_routes
from api.config import init_config_routes
from api.matches.matches import init_match_routes
from api.matches.actions import init_match_action_routes
from api.matches.players import init_match_player_routes
from api.rounds import init_round_routes
from api.matches.events import events_blueprint
import logging
from logging.handlers import RotatingFileHandler

# Configure logging
log_formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')

# Log to a file
file_handler = RotatingFileHandler('app.log', maxBytes=1000000, backupCount=3)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(log_formatter)

# Log to console
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(log_formatter)

# Get the root logger
root_logger = logging.getLogger()
root_logger.setLevel(logging.INFO)
root_logger.addHandler(file_handler)
root_logger.addHandler(console_handler)

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-very-secret-key'  # Change this to a real secret in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 600  # seconds
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 2419200  # seconds

CORS(app)

jwt = JWTManager(app)

init_auth_routes(app)
init_card_routes(app)
init_match_routes(app)
init_match_action_routes(app)
init_match_player_routes(app)
init_round_routes(app)
init_config_routes(app)

app.register_blueprint(events_blueprint, url_prefix='/')

if __name__ == '__main__':
    app.run(debug=True)
