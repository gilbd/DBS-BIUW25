from controllers.nutrition_controller import nutrition_controller
from flask import Blueprint

# Define the Blueprint for nutrition routes
nutrition_routes = Blueprint("nutrition_routes", __name__)

# Register the routes from the nutrition_controller Blueprint
nutrition_routes.register_blueprint(nutrition_controller)
