from flask import Blueprint, request, jsonify
from app import db
from app.models.relationships.contains import Contains
from app.models.recipe import Recipe
from app.models.nutrition import Nutrition

contains_controller = Blueprint('contains_controller', __name__)

# Add nutrition to a recipe
@contains_controller.route('/contains', methods=['POST'])
def add_nutrition_to_recipe():
    recipe_id = request.json.get('recipe_id')
    nutrition_name = request.json.get('nutrition_name')
    amount = request.json.get('amount')
    
    recipe = Recipe.query.get(recipe_id)
    nutrition = Nutrition.query.get(nutrition_name)
    
    if recipe and nutrition:
        contains = Contains(recipe_id=recipe_id, nutrition_name=nutrition_name, amount=amount)
        db.session.add(contains)
        db.session.commit()
        return jsonify(contains.to_dict()), 201
    return jsonify({"error": "Recipe or Nutrition not found"}), 404