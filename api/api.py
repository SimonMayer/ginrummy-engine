from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from api.cards import init_card_routes
from api.matches.matches import init_matches
from api.matches.players import init_match_players
from api.rounds import init_round_routes
from api.sign_in import init_auth_routes
from api.turns import init_turn_routes

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-very-secret-key'  # Change this to a real secret in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 600  # seconds
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 2419200  # seconds

app.config['MIN_PLAYERS'] = 2
app.config['MAX_PLAYERS'] = 4
app.config['HAND_SIZE'] = 7
app.config['POINTS_BY_RANK'] = {
   'A': 15,
   '2': 2,
   '3': 3,
   '4': 4,
   '5': 5,
   '6': 6,
   '7': 7,
   '8': 8,
   '9': 9,
   '10': 10,
   'J': 10,
   'Q': 10,
   'K': 10
}

CORS(app)

jwt = JWTManager(app)

init_auth_routes(app)
init_card_routes(app)
init_matches(app)
init_match_players(app)
init_round_routes(app)
init_turn_routes(app)

if __name__ == '__main__':
    app.run(debug=True)
