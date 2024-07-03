from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from api.matches import init_matches
from api.sign_in import init_auth_routes

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-very-secret-key'  # Change this to a real secret in production
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 600 # seconds
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 2419200 # seconds

app.config['MIN_PLAYERS'] = 2
app.config['MAX_PLAYERS'] = 4

CORS(app)

jwt = JWTManager(app)

# Initialize authentication and match routes
init_auth_routes(app)
init_matches(app)

if __name__ == '__main__':
    app.run(debug=True)
