from flask import Flask
from routes import (
    admin_routes,
    contains_routes,
    diet_routes,
    eats_routes,
    fits_routes,
    nutrition_routes,
    rating_routes,
    recipe_routes,
    user_diet_routes,
    user_nutrition_routes,
    user_routes,
)


def create_app():
    app = Flask(__name__)

    # Register all the routes (Blueprints) for the app
    app.register_blueprint(admin_routes, url_prefix='/api')
    app.register_blueprint(contains_routes, url_prefix='/api')
    app.register_blueprint(diet_routes, url_prefix='/api')
    app.register_blueprint(eats_routes, url_prefix='/api')
    app.register_blueprint(fits_routes, url_prefix='/api')
    app.register_blueprint(nutrition_routes, url_prefix='/api')
    app.register_blueprint(rating_routes, url_prefix='/api')
    app.register_blueprint(recipe_routes, url_prefix='/api')
    app.register_blueprint(user_routes, url_prefix='/api')
    app.register_blueprint(user_diet_routes, url_prefix='/api')
    app.register_blueprint(user_nutrition_routes, url_prefix='/api')

    return app    return app