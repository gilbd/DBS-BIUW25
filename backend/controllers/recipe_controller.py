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
        # Get user_id from request args or JWT token
        user_id = request.args.get('user_id')
        
        # Get 5 random recipes
        random_recipes = Recipe.query.order_by(func.random()).limit(5).all()
        
        # Convert recipes to dictionary format with user_id context
        recipes_data = [recipe.to_dict(user_id=user_id) for recipe in random_recipes]
        
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


@recipe_controller.route('/new-recommendation', methods=['GET'])
def get_new_recommendation():
    try:
        user_id = request.args.get('user_id')
        if not user_id:
            return jsonify({
                'status': 'error',
                'message': 'User ID is required'
            }), 400
        
        # Get one random recipe that hasn't been eaten by this user
        new_recipe = (
            Recipe.query
            .outerjoin(Eats)
            .filter(
                ~Recipe.eats.any(Eats.user_id == user_id)  # Not eaten by this user
            )
            .order_by(func.random())
            .first()
        )
        
        if not new_recipe:
            return jsonify({
                'status': 'error',
                'message': 'No new recipes available'
            }), 404
        
        return jsonify({
            'status': 'success',
            'data': new_recipe.to_dict(user_id=user_id)
        }), 200

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500


@recipe_controller.route('/search', methods=['GET'])
def search_recipes():
    try:
        max_time = request.args.get('maxTime')
        query = request.args.get('query')
        diet = request.args.get('diet')
        ingredient = request.args.get('ingredient')
        
        # Build the query
        query_obj = Recipe.query
        
        # Apply filters if provided
        if max_time and max_time.isdigit():
            query_obj = query_obj.filter(Recipe.total_time <= int(max_time))
            
        if query:
            # Split the search query into words and search for all words in the recipe name
            search_words = query.lower().split()
            for word in search_words:
                search = f"%{word}%"
                query_obj = query_obj.filter(Recipe.recipe_name.ilike(search))
            
        if ingredient:
            # Search in ingredients field
            search = f"%{ingredient}%"
            query_obj = query_obj.filter(Recipe.ingredients.ilike(search))
            
        if diet:
            search = f"%{diet}%"
            query_obj = query_obj.filter(Recipe.diets.ilike(search))
        
        # Get 4 random recipes that match the criteria
        recipes = query_obj.order_by(func.random()).limit(4).all()
        
        # Convert to dictionary format
        recipes_data = [recipe.to_dict() for recipe in recipes]
        
        return jsonify({
            'status': 'success',
            'data': recipes_data
        }), 200

    except Exception as e:
        print(f"Search error: {e}")  # Add logging for debugging
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500