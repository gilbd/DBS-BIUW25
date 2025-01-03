from flask import Blueprint
from app.controllers.admin_controller import admin_controller

# Define the Blueprint for admin routes
admin_routes = Blueprint('admin_routes', __name__)

# Register the routes from the admin_controller Blueprint
admin_routes.register_blueprint(admin_controller)