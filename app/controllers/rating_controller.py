from flask import Blueprint, request, jsonify
from app import db
from app.models.relationships.rating import Rating
from app.models.recipe import Recipe
from app.models.user import User

rating_controller = Blueprint('rating_controller', __name__)

# Rate a recipe
@rating_controller.route('/ratings', methods=['POST'])
def rate_recipe():
    user_id = request.json.get('user_id')
    recipe_id = request.json.get('recipe_id')
    rating = request.json.get('rating')
    
    user = User.query.get(user_id)
    recipe = Recipe.query.get(recipe_id)
    
    if user and recipe:
        new_rating = Rating(user_id=user_id, recipe_id=recipe_id, rating=rating)
        db.session.add(new_rating)
        db.session.commit()
        return jsonify(new_rating.to_dict()), 201
    return jsonify({"error": "User or Recipe not found"}), 404