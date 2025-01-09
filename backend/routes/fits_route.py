from flask import Blueprint
from app.controllers.fits_controller import fits_controller

# Define the Blueprint for fits routes
fits_routes = Blueprint('fits_routes', __name__)

# Register the routes from the fits_controller Blueprint
fits_routes.register_blueprint(fits_controller)