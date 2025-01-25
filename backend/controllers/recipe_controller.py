import logging

from config.database import db
from flask import Blueprint, jsonify, request
from models.recipe import Recipe
from models.relationships.eats import Eats
from sqlalchemy.sql import text

logger = logging.getLogger(__name__)

recipe_controller = Blueprint("recipe_controller", __name__)


# Create new recipe
@recipe_controller.route("/recipes", methods=["POST"])
def create_recipe():
    data = request.get_json()
    query = """
        INSERT INTO recipe (recipe_name, total_time, image, directions, ingredients)
        VALUES (:recipe_name, :total_time, :image, :directions, :ingredients)
        RETURNING *;
    """
    result = db.session.execute(
        text(query),
        {
            "recipe_name": data["recipe_name"],
            "total_time": data["total_time"],
            "image": data.get("image", ""),
            "directions": data["directions"],
            "ingredients": data["ingredients"],
        },
    )
    db.session.commit()
    recipe = Recipe.query.get(result.first()[0])
    return jsonify(recipe.to_dict()), 201


# Get recipe according id
@recipe_controller.route("/recipes/<int:id>", methods=["GET"])
def get_recipe(id):
    query = "SELECT * FROM recipe WHERE recipe_id = :id"
    result = db.session.execute(text(query), {"id": id}).first()
    if result:
        recipe = Recipe.query.get(result[0])
        return jsonify(recipe.to_dict()), 200
    logger.error(f"Recipe not found for retrieval: {id}")
    return jsonify({"message": "Recipe not found"}), 404


# Update recipe according id
@recipe_controller.route("/recipes/<int:id>", methods=["PUT"])
def update_recipe(id):
    data = request.get_json()
    query = """
        UPDATE recipe 
        SET recipe_name = :recipe_name,
            total_time = :total_time,
            image = :image,
            directions = :directions,
            ingredients = :ingredients
        WHERE recipe_id = :id
        RETURNING *;
    """
    result = db.session.execute(
        text(query),
        {
            "id": id,
            "recipe_name": data.get("recipe_name"),
            "total_time": data.get("total_time"),
            "image": data.get("image"),
            "directions": data.get("directions"),
            "ingredients": data.get("ingredients"),
        },
    ).first()
    if result:
        db.session.commit()
        recipe = Recipe.query.get(result[0])
        return jsonify(recipe.to_dict()), 200
    logger.error(f"Recipe not found for update: {id}")
    return jsonify({"message": "Recipe not found"}), 404


# Delete recipe according id
@recipe_controller.route("/recipes/<int:id>", methods=["DELETE"])
def delete_recipe(id):
    query = "DELETE FROM recipe WHERE recipe_id = :id RETURNING recipe_id"
    result = db.session.execute(text(query), {"id": id}).first()
    if result:
        db.session.commit()
        return jsonify({"message": "Recipe deleted"}), 200
    logger.error(f"Recipe not found for deletion: {id}")
    return jsonify({"message": "Recipe not found"}), 404


@recipe_controller.route("/recommendations", methods=["GET"])
def get_recommendations():
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            logger.error("User ID is required")
            return jsonify({"status": "error", "message": "User ID is required"}), 400

        query = """
            SELECT r.* FROM recipe r
            WHERE NOT EXISTS (
                SELECT 1 FROM eats e
                WHERE e.recipe_id = r.recipe_id
                AND e.user_id = :user_id
            )
            ORDER BY RAND()
            LIMIT 5;
        """
        result = db.session.execute(text(query), {"user_id": user_id})
        recipes = [Recipe.query.get(row[0]) for row in result]
        recipes_data = [recipe.to_dict(user_id=user_id) for recipe in recipes]

        return jsonify({"status": "success", "data": recipes_data}), 200

    except Exception as e:
        logger.error(f"Error in get_recommendations: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@recipe_controller.route("/recent", methods=["GET"])
def get_recent_recipes():
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            logger.error("User ID is required")
            return jsonify({"status": "error", "message": "User ID is required"}), 400

        query = """
            SELECT r.* 
            FROM recipe r
            JOIN eats e ON r.recipe_id = e.recipe_id
            WHERE e.user_id = :user_id
            GROUP BY r.recipe_id
            ORDER BY MAX(e.created_at) DESC
            LIMIT 3;
        """
        result = db.session.execute(text(query), {"user_id": user_id})
        recipes = [Recipe.query.get(row[0]) for row in result]
        recipes_data = [recipe.to_dict(user_id=user_id) for recipe in recipes]

        return jsonify({"status": "success", "data": recipes_data}), 200

    except Exception as e:
        logger.error(f"Error in get_recent_recipes: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@recipe_controller.route("/new-recommendation", methods=["GET"])
def get_new_recommendation():
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"status": "error", "message": "User ID is required"}), 400

        query = """
            SELECT r.* FROM recipe r
            WHERE NOT EXISTS (
                SELECT 1 FROM eats e
                WHERE e.recipe_id = r.recipe_id
                AND e.user_id = :user_id
            )
            ORDER BY RAND()
            LIMIT 1;
        """
        result = db.session.execute(text(query), {"user_id": user_id}).first()

        if not result:
            logger.error("No new recipes available")
            return jsonify({"status": "error", "message": "No new recipes available"}), 404

        recipe = Recipe.query.get(result[0])
        return jsonify({"status": "success", "data": recipe.to_dict(user_id=user_id)}), 200

    except Exception as e:
        logger.error(f"Error in get_new_recommendation: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@recipe_controller.route("/search", methods=["GET"])
def search_recipes():
    try:
        max_time = request.args.get("maxTime")
        query_str = request.args.get("query")
        diet = request.args.get("diet")
        ingredient = request.args.get("ingredient")

        base_query = """
            SELECT DISTINCT r.* 
            FROM recipe r
        """

        conditions = []
        params = {}

        if diet:
            base_query += """
                JOIN fits f ON r.recipe_id = f.recipe_id
                JOIN diet d ON f.diet_id = d.diet_id
            """
            conditions.append("d.name = :diet")
            params["diet"] = diet

        conditions.append("1=1")

        if max_time and max_time.isdigit():
            conditions.append("r.total_time <= :max_time")
            params["max_time"] = int(max_time)

        if query_str:
            search_words = query_str.lower().split()
            for i, word in enumerate(search_words):
                param_name = f"word_{i}"
                conditions.append(f"LOWER(r.recipe_name) LIKE :{param_name}")
                params[param_name] = f"%{word}%"

        if ingredient:
            conditions.append("LOWER(r.ingredients) LIKE :ingredient")
            params["ingredient"] = f"%{ingredient.lower()}%"

        if conditions:
            base_query += " WHERE " + " AND ".join(conditions)

        base_query += " ORDER BY RAND() LIMIT 4"

        logger.info(f"Executing query: {base_query} with params: {params}")

        result = db.session.execute(text(base_query), params)
        recipes = [Recipe.query.get(row[0]) for row in result]
        recipes_data = [recipe.to_dict() for recipe in recipes]

        return jsonify({"status": "success", "data": recipes_data}), 200

    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500
