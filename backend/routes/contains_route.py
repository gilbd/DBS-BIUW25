from controllers.contains_controller import contains_controller
from flask import Blueprint

# Define the Blueprint for contains routes
contains_routes = Blueprint("contains_routes", __name__)

# Register the routes from the contains_controller Blueprint
contains_routes.register_blueprint(contains_controller)
