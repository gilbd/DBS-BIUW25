from flask import Blueprint
from app.controllers.eats_controller import eats_controller

# Define the Blueprint for eats routes
eats_routes = Blueprint('eats_routes', __name__)

# Register the routes from the eats_controller Blueprint
eats_routes.register_blueprint(eats_controller)