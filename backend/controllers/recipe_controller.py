import logging

from config.database import db
from flask import Blueprint, jsonify, request
from models.recipe import Recipe
from models.relationships.eats import Eats
from sqlalchemy.sql import text

logger = logging.getLogger(__name__)

recipe_controller = Blueprint("recipe_controller", __name__)


# Create new recipe
@recipe_controller.route("/", methods=["POST"])
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
@recipe_controller.route("/<int:id>", methods=["GET"])
def get_recipe(id):
    try:
        user_id = request.args.get("user_id")
        logger.info(f"Getting recipe {id} for user {user_id}")

        query = """
            SELECT 
                r.*,
                CASE WHEN e.user_id IS NOT NULL THEN TRUE ELSE FALSE END as is_eaten,
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'name', n.name,
                        'amount', c.amount,
                        'unit', n.unit
                    )
                ) as nutrition_info
            FROM recipe r
            LEFT JOIN eats e ON r.recipe_id = e.recipe_id AND e.user_id = :user_id
            LEFT JOIN contains c ON r.recipe_id = c.recipe_id
            LEFT JOIN nutrition n ON c.nutrition_name = n.name
            WHERE r.recipe_id = :id
            GROUP BY r.recipe_id, e.user_id
        """

        result = db.session.execute(text(query), {"id": id, "user_id": user_id}).first()

        if not result:
            logger.error(f"Recipe {id} not found")
            return jsonify({"status": "error", "message": "Recipe not found"}), 404

        # Parse nutrition_info from string to list if it exists and isn't null
        nutrition_info = []
        if result.nutrition_info:
            try:
                import json

                nutrition_info = json.loads(result.nutrition_info)
                # Filter out null entries
                nutrition_info = [n for n in nutrition_info if n.get("name") is not None]
            except Exception as e:
                logger.error(f"Error parsing nutrition info: {e}")

        recipe_data = {
            "recipe_id": result.recipe_id,
            "recipe_name": result.recipe_name,
            "ingredients": result.ingredients,
            "directions": result.directions,
            "total_time": result.total_time,
            "image": result.image,
            "is_eaten": bool(result.is_eaten),
            "nutrition_info": nutrition_info,
        }

        logger.info(f"Recipe data: {recipe_data}")
        return jsonify({"status": "success", "data": recipe_data})

    except Exception as e:
        logger.error(f"Error getting recipe: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


# Update recipe according id
@recipe_controller.route("/<int:id>", methods=["PUT"])
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
@recipe_controller.route("/<int:id>", methods=["DELETE"])
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
            SELECT r.recipe_id
            FROM recipe r
            WHERE NOT EXISTS (
                SELECT 1 FROM eats e2
                WHERE e2.recipe_id = r.recipe_id
                AND e2.user_id = :user_id
            )
            ORDER BY RAND()
            LIMIT 5;
        """

        result = db.session.execute(text(query), {"user_id": user_id})
        recipe_ids = [row.recipe_id for row in result]

        return jsonify({"status": "success", "data": recipe_ids}), 200

    except Exception as e:
        logger.error(f"Error getting recommendations: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@recipe_controller.route("/recent", methods=["GET"])
def get_recent_recipes():
    try:
        user_id = request.args.get("user_id")
        if not user_id:
            return jsonify({"status": "error", "message": "User ID is required"}), 400

        query = """
            SELECT r.recipe_id, latest_e.latest_created_at
            FROM recipe r
            JOIN (
                SELECT e.recipe_id, MAX(e.created_at) AS latest_created_at
                FROM eats e
                WHERE e.user_id = :user_id
                GROUP BY e.recipe_id
            ) latest_e ON r.recipe_id = latest_e.recipe_id
            ORDER BY latest_e.latest_created_at DESC
            LIMIT 4;
        """

        result = db.session.execute(text(query), {"user_id": user_id})
        recipe_ids = [row.recipe_id for row in result]

        return jsonify({"status": "success", "data": recipe_ids}), 200

    except Exception as e:
        logger.error(f"Error getting recent recipes: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@recipe_controller.route("/search", methods=["GET"])
def search_recipes():
    try:
        max_time = request.args.get("maxTime")
        query_str = request.args.get("query")
        diet = request.args.get("diet")
        ingredient = request.args.get("ingredient")
        user_id = request.args.get("user_id")

        base_query = """
            SELECT DISTINCT 
                r.*,
                CASE WHEN e.user_id IS NOT NULL THEN TRUE ELSE FALSE END as is_eaten
            FROM recipe r
            LEFT JOIN eats e ON r.recipe_id = e.recipe_id AND e.user_id = :user_id
        """

        conditions = []
        params = {"user_id": user_id}

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
        recipes_data = [
            {
                "recipe_id": row.recipe_id,
                "recipe_name": row.recipe_name,
                "ingredients": row.ingredients,
                "directions": row.directions,
                "total_time": row.total_time,
                "image": row.image,
                "is_eaten": bool(row.is_eaten),
            }
            for row in result
        ]

        return jsonify({"status": "success", "data": recipes_data}), 200

    except Exception as e:
        logger.error(f"Search error: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


@recipe_controller.route("/<int:recipe_id>", methods=["GET"])
def get_recipe_with_status(recipe_id):
    try:
        user_id = request.args.get("user_id")
        logger.info(f"Getting recipe {recipe_id} for user {user_id}")

        query = """
            SELECT 
                r.*,
                CASE WHEN e.user_id IS NOT NULL THEN TRUE ELSE FALSE END as is_eaten,
                JSON_ARRAYAGG(
                    JSON_OBJECT(
                        'name', n.name,
                        'amount', c.amount,
                        'unit', n.unit
                    )
                ) as nutrition_info
            FROM recipe r
            LEFT JOIN eats e ON r.recipe_id = e.recipe_id AND e.user_id = :user_id
            LEFT JOIN contains c ON r.recipe_id = c.recipe_id
            LEFT JOIN nutrition n ON c.nutrition_name = n.name
            WHERE r.recipe_id = :recipe_id
            GROUP BY r.recipe_id, e.user_id
        """

        result = db.session.execute(
            text(query), {"recipe_id": recipe_id, "user_id": user_id}
        ).first()

        if not result:
            logger.error(f"Recipe {recipe_id} not found")
            return jsonify({"status": "error", "message": "Recipe not found"}), 404

        # Parse nutrition_info from string to list if it exists and isn't null
        nutrition_info = []
        if result.nutrition_info:
            try:
                import json

                nutrition_info = json.loads(result.nutrition_info)
                # Filter out null entries
                nutrition_info = [n for n in nutrition_info if n.get("name") is not None]
            except Exception as e:
                logger.error(f"Error parsing nutrition info: {e}")

        recipe_data = {
            "recipe_id": result.recipe_id,
            "recipe_name": result.recipe_name,
            "ingredients": result.ingredients,
            "directions": result.directions,
            "total_time": result.total_time,
            "image": result.image,
            "is_eaten": bool(result.is_eaten),
            "nutrition_info": nutrition_info,
        }

        logger.info(f"Recipe data: {recipe_data}")
        return jsonify({"status": "success", "data": recipe_data})

    except Exception as e:
        logger.error(f"Error getting recipe: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500
