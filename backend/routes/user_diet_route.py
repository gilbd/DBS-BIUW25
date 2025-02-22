from controllers.user_diet_controller import user_diet_controller
from flask import Blueprint

# Define the Blueprint for user_diet routes
user_diet_routes = Blueprint("user_diet_routes", __name__)

# Register the routes from the user_diet_controller Blueprint
user_diet_routes.register_blueprint(user_diet_controller)
