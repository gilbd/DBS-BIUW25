from config.database import db
from config.settings import (
    DEBUG,
    SECRET_KEY,
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS,
)
from flask import Flask
from flask_cors import CORS
from sqlalchemy.sql import text


def create_app():
    app = Flask(__name__)
    
    # Configure CORS
    CORS(app, resources={
        r"/api/*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST", "PUT", "DELETE"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    # Application configurations
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["DEBUG"] = DEBUG
    app.config["SECRET_KEY"] = SECRET_KEY

    # Initialize extensions
    db.init_app(app)

    # Create tables if not exist
    with app.app_context():
        db.create_all()
        # Test database connection
        try:
            test = db.session.execute(text("SELECT 1")).scalar()
            assert test == 1, "Database connection error"
            print("Database connection successful!")
        except Exception as e:
            print(f"Database connection failed: {e}")

        # Import and register blueprints
        from controllers.admin_controller import admin_controller
        from controllers.auth_controller import auth_controller
        from controllers.user_controller import user_controller
        from controllers.recipe_controller import recipe_controller
        from controllers.eats_controller import eats_controller

        app.register_blueprint(admin_controller, url_prefix="/api/admin")
        app.register_blueprint(auth_controller, url_prefix="/api/auth")
        app.register_blueprint(user_controller, url_prefix="/api/user")
        app.register_blueprint(recipe_controller, url_prefix="/api/recipes")
        app.register_blueprint(eats_controller, url_prefix="/api/eats")

        # app.register_blueprint(auth_controller, url_prefix="/api/auth")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="localhost", port=5000, debug=True)
