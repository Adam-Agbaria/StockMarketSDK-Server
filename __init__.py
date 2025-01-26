from flask import Flask
from flask_restful import Api
from app.routes import initialize_routes

# Initialize Flask app
app = Flask(__name__)

# Initialize Flask-RESTful API
api = Api(app)

# Register routes
initialize_routes(api)

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
