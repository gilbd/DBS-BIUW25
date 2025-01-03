from flask import Blueprint
from app.controllers.diet_controller import diet_controller

# Define the Blueprint for diet routes
diet_routes = Blueprint('diet_routes', __name__)

# Register the routes from the diet_controller Blueprint
diet_routes.register_blueprint(diet_controller)