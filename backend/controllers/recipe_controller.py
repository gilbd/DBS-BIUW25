from config.database import db
from flask import Blueprint, jsonify, request
from models.recipe import Recipe
from sqlalchemy.sql import func
from models.relationships.eats import Eats

recipe_controller = Blueprint("recipe_controller", __name__)


# Create new recipe
@recipe_controller.route("/recipes", methods=["POST"])
def create_recipe():
    data = request.get_json()
    new_recipe = Recipe(
        recipe_name=data["recipe_name"],
        total_time=data["total_time"],
        image=data.get("image", ""),
        directions=data["directions"],
        ingredients=data["ingredients"],
    )
    db.session.add(new_recipe)
    db.session.commit()
    return jsonify(new_recipe.to_dict()), 201


# Get recipe according id
@recipe_controller.route("/recipes/<int:id>", methods=["GET"])
def get_recipe(id):
    recipe = Recipe.query.get(id)
    if recipe:
        return jsonify(recipe.to_dict()), 200
    return jsonify({"message": "Recipe not found"}), 404


# Update recipe according id
@recipe_controller.route("/recipes/<int:id>", methods=["PUT"])
def update_recipe(id):
    data = request.get_json()
    recipe = Recipe.query.get(id)
    if recipe:
        recipe.recipe_name = data.get("recipe_name", recipe.recipe_name)
        recipe.total_time = data.get("total_time", recipe.total_time)
        recipe.image = data.get("image", recipe.image)
        recipe.directions = data.get("directions", recipe.directions)
        recipe.ingredients = data.get("ingredients", recipe.ingredients)
        db.session.commit()
        return jsonify(recipe.to_dict()), 200
    return jsonify({"message": "Recipe not found"}), 404


# Delete recipe according id
@recipe_controller.route("/recipes/<int:id>", methods=["DELETE"])
def delete_recipe(id):
    recipe = Recipe.query.get(id)
    if recipe:
        db.session.delete(recipe)
        db.session.commit()
        return jsonify({"message": "Recipe deleted"}), 200
    return jsonify({"message": "Recipe not found"}), 404


@recipe_controller.route('/recommendations', methods=['GET'])
def get_recommendations():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({
                'status': 'error',
                'message': 'User ID is required'
            }), 400
        
        # Get recipes that the user hasn't eaten yet
        uneaten_recipes = (
            Recipe.query
            .outerjoin(Eats)
            .filter(
                (Eats.user_id.is_(None)) |  # Recipe has no eats records
                (Eats.user_id != user_id)    # Or not eaten by this user
            )
            .order_by(func.random())
            .limit(3)
            .all()
        )
        
        # Convert recipes to dictionary format with user_id context
        recipes_data = [recipe.to_dict(user_id=user_id) for recipe in uneaten_recipes]
        
        return jsonify({
            'status': 'success',
            'data': recipes_data
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@recipe_controller.route('/recent', methods=['GET'])
def get_recent_recipes():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({
                'status': 'error',
                'message': 'User ID is required'
            }), 400

        # Get recent recipes eaten by the user, ordered by most recent first
        recent_recipes = (
            Recipe.query
            .join(Recipe.eats)
            .filter(Eats.user_id == user_id)
            .order_by(Eats.created_at.desc())
            .limit(3)
            .all()
        )
        
        # Convert recipes to dictionary format with user_id context
        recipes_data = [recipe.to_dict(user_id=user_id) for recipe in recent_recipes]
        
        return jsonify({
            'status': 'success',
            'data': recipes_data
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500