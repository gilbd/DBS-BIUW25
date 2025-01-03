from flask import Blueprint
from app.controllers.user_controller import user_controller

# Define the Blueprint for user routes
user_routes = Blueprint('user_routes', __name__)

# Register the routes from the user_controller Blueprint
user_routes.register_blueprint(user_controller)