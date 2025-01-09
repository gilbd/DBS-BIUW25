from flask import Blueprint
from app.controllers.user_nutrition_controller import user_nutrition_controller

# Define the Blueprint for user_nutrition routes
user_nutrition_routes = Blueprint('user_nutrition_routes', __name__)

# Register the routes from the user_nutrition_controller Blueprint
user_nutrition_routes.register_blueprint(user_nutrition_controller)