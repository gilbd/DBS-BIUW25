from controllers.rating_controller import rating_controller
from flask import Blueprint

# Define the Blueprint for rating routes
rating_routes = Blueprint("rating_routes", __name__)

# Register the routes from the rating_controller Blueprint
rating_routes.register_blueprint(rating_controller)
