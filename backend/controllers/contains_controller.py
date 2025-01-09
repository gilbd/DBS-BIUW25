from config.database import db
from flask import Blueprint, jsonify, request
from models.nutrition import Nutrition
from models.recipe import Recipe
from models.relationships.contains import Contains

contains_controller = Blueprint("contains_controller", __name__)


# Add nutrition to a recipe
@contains_controller.route("/contains", methods=["POST"])
def add_nutrition_to_recipe():
    recipe_id = request.json.get("recipe_id")
    nutrition_name = request.json.get("nutrition_name")
    amount = request.json.get("amount")

    recipe = db.session.execute(
        "SELECT * FROM recipe WHERE recipe_id = :recipe_id", {"recipe_id": recipe_id}
    ).fetchone()
    nutrition = db.session.execute(
        "SELECT * FROM nutrition WHERE nutrition_name = :nutrition_name",
        {"nutrition_name": nutrition_name},
    ).fetchone()

    if recipe and nutrition:
        contains = Contains(recipe_id=recipe_id, nutrition_name=nutrition_name, amount=amount)
        db.session.add(contains)
        db.session.commit()
        return jsonify(contains.to_dict()), 201
    return jsonify({"error": "Recipe or Nutrition not found"}), 404
