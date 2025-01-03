from flask import Blueprint, request, jsonify
from app import db
from app.models.relationships.fits import Fits
from app.models.recipe import Recipe
from app.models.diet import Diet

fits_controller = Blueprint('fits_controller', __name__)

# Assign a recipe to a diet
@fits_controller.route('/fits', methods=['POST'])
def add_recipe_to_diet():
    recipe_id = request.json.get('recipe_id')
    diet_id = request.json.get('diet_id')
    
    recipe = Recipe.query.get(recipe_id)
    diet = Diet.query.get(diet_id)
    
    if recipe and diet:
        fits = Fits(recipe_id=recipe_id, diet_id=diet_id)
        db.session.add(fits)
        db.session.commit()
        return jsonify(fits.to_dict()), 201
    return jsonify({"error": "Recipe or Diet not found"}), 404