from flask import Flask
from config.database import db
from config.settings import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_TRACK_MODIFICATIONS, DEBUG, SECRET_KEY

def create_app():
    app = Flask(__name__)

    # Application configurations
    app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = SQLALCHEMY_TRACK_MODIFICATIONS
    app.config['DEBUG'] = DEBUG
    app.config['SECRET_KEY'] = SECRET_KEY

    # Initialize extensions
    db.init_app(app)

    # Create tables if not exist
    with app.app_context():
        db.create_all()

    return app