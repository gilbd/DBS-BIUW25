from controllers.recipe_controller import recipe_controller
from flask import Blueprint

# Define the Blueprint for recipe routes
recipe_routes = Blueprint("recipe_routes", __name__)

# Register the routes from the recipe_controller Blueprint
recipe_routes.register_blueprint(recipe_controller)
