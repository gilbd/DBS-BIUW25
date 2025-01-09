from flask import Flask
from config.database import db
from config.settings import (
    SQLALCHEMY_DATABASE_URI,
    SQLALCHEMY_TRACK_MODIFICATIONS,
    DEBUG,
    SECRET_KEY,
)


def create_app():
    app = Flask(__name__)

    # Application configurations
    app.config["SQLALCHEMY_DATABASE_URI"] = SQLALCHEMY_DATABASE_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["DEBUG"] = DEBUG
    app.config["SECRET_KEY"] = SECRET_KEY

    # Initialize extensions
    db.init_app(app)

    # Create tables if not exist
    with app.app_context():
        # Import models to ensure they're known to SQLAlchemy
        from models.user import User
        from models.admin import Admin

        db.create_all()

        # Import and register blueprints
        from controllers.auth_controller import auth_controller

        app.register_blueprint(auth_controller, url_prefix="/api/auth")

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True, host="0.0.0.0", port=5000)
