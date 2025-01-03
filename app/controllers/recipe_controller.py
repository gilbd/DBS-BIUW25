from flask import Blueprint, request, jsonify
from app import db
from app.models.recipe import Recipe

recipe_controller = Blueprint('recipe_controller', __name__)

# Create new recipe
@recipe_controller.route('/recipes', methods=['POST'])
def create_recipe():
    data = request.get_json()
    new_recipe = Recipe(
        recipe_name=data['recipe_name'],
        total_time=data['total_time'],
        image=data.get('image', ''),
        directions=data['directions'],
        ingredients=data['ingredients']
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify(new_recipe.to_dict()), 201

# Get recipe according id
@recipe_controller.route('/recipes/<int:id>', methods=['GET'])
def get_recipe(id):
    recipe = Recipe.query.get(id)
    if recipe:
        return jsonify(recipe.to_dict()), 200
    return jsonify({'message': 'Recipe not found'}), 404

# Update recipe according id
@recipe_controller.route('/recipes/<int:id>', methods=['PUT'])
def update_recipe(id):
    data = request.get_json()
    recipe = Recipe.query.get(id)
    if recipe:
        recipe.recipe_name = data.get('recipe_name', recipe.recipe_name)
        recipe.total_time = data.get('total_time', recipe.total_time)
        recipe.image = data.get('image', recipe.image)
        recipe.directions = data.get('directions', recipe.directions)
        recipe.ingredients = data.get('ingredients', recipe.ingredients)
        db.session.commit()
        return jsonify(recipe.to_dict()), 200
    return jsonify({'message': 'Recipe not found'}), 404

# Delete recipe according id
@recipe_controller.route('/recipes/<int:id>', methods=['DELETE'])
def delete_recipe(id):
    recipe = Recipe.query.get(id)
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        return jsonify({'message': 'Recipe deleted'}), 200
    return jsonify({'message': 'Recipe not found'}), 404