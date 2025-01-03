from flask import Flask
from app.routes import db
from app.controllers import (
    recipe_controller,
    user_controller,
    admin_controller,
    diet_controller,
    nutrition_controller,
    user_diet_controller,
    user_nutrition_controller,
    eats_controller,
    rating_controller,
    contains_controller,
    fits_controller,
)
from config.settings import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, DEBUG, SECRET_KEY


def create_app():
    app = Flask(__name__)
    
    # Load configuration from settings.py
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['DEBUG'] = DEBUG
    app.config['SECRET_KEY'] = SECRET_KEY

    # Initialize database
    db.init_app(app)

    # Register Blueprints
    app.register_blueprint(recipe_controller, url_prefix='/api/recipes')
    app.register_blueprint(user_controller, url_prefix='/api/users')
    app.register_blueprint(admin_controller, url_prefix='/api/admins')
    app.register_blueprint(diet_controller, url_prefix='/api/diets')
    app.register_blueprint(nutrition_controller, url_prefix='/api/nutrition')
    app.register_blueprint(user_diet_controller, url_prefix='/api/user-diets')
    app.register_blueprint(user_nutrition_controller, url_prefix='/api/user-nutrition')
    app.register_blueprint(eats_controller, url_prefix='/api/eats')
    app.register_blueprint(rating_controller, url_prefix='/api/ratings')
    app.register_blueprint(contains_controller, url_prefix='/api/contains')
    app.register_blueprint(fits_controller, url_prefix='/api/fits')

    return app