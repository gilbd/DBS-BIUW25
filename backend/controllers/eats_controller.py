from config.database import db
from flask import Blueprint, jsonify, request
from models.recipe import Recipe
from models.relationships.eats import Eats
from models.user import User

eats_controller = Blueprint("eats_controller", __name__)


# Log when a user eats a recipe
@eats_controller.route("/eats", methods=["POST"])
def log_user_eats():
    user_id = request.json.get("user_id")
    recipe_id = request.json.get("recipe_id")

    user = User.query.get(user_id)
    recipe = Recipe.query.get(recipe_id)

    if user and recipe:
        eats = Eats(user_id=user_id, recipe_id=recipe_id)
        db.session.add(eats)
        db.session.commit()
        return jsonify(eats.to_dict()), 201
    return jsonify({"error": "User or Recipe not found"}), 404
