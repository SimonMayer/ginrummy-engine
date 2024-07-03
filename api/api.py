from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from api.matches import init_matches
from api.sign_in import init_auth_routes

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-very-secret-key'  # Change this to a real secret in production

CORS(app)

jwt = JWTManager(app)

# Initialize authentication and match routes
init_auth_routes(app)
init_matches(app)

if __name__ == '__main__':
    app.run(debug=True)
