import logging
from datetime import datetime, timezone

from config.database import db
from flask import Blueprint, jsonify, request
from models.recipe import Recipe
from models.user import User
from sqlalchemy.sql import text
from utils.auth import token_required

logger = logging.getLogger(__name__)

rating_controller = Blueprint("rating_controller", __name__)


@rating_controller.route("/rate", methods=["POST"])
@token_required
def rate_recipe(current_user):
    try:
        data = request.get_json()
        logger.info(f"Rating recipe: {data}")

        # Validate input
        user_id = current_user.user_id
        recipe_id = data.get("recipe_id")
        rating = data.get("rating")

        if not recipe_id or not rating:
            return jsonify({"error": "Missing recipe_id or rating"}), 400

        if not isinstance(rating, int) or rating < 1 or rating > 5:
            return jsonify({"error": "Rating must be between 1 and 5"}), 400

        # Check if user has eaten this recipe
        has_eaten = db.session.execute(
            text(
                """
                SELECT 1 FROM eats 
                WHERE user_id = :user_id AND recipe_id = :recipe_id
                LIMIT 1
            """
            ),
            {"user_id": user_id, "recipe_id": recipe_id},
        ).scalar()

        if not has_eaten:
            return jsonify({"error": "You can only rate recipes you have eaten"}), 403

        # Insert or update rating
        created_at = datetime.now(timezone.utc)
        query = """
            INSERT INTO rating (user_id, recipe_id, rating, created_at)
            VALUES (:user_id, :recipe_id, :rating, :created_at)
            ON DUPLICATE KEY UPDATE 
                rating = :rating,
                created_at = :created_at
        """
        db.session.execute(
            text(query),
            {
                "user_id": user_id,
                "recipe_id": recipe_id,
                "rating": rating,
                "created_at": created_at,
            },
        )
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "message": "Rating saved successfully",
                    "data": {
                        "user_id": user_id,
                        "recipe_id": recipe_id,
                        "rating": rating,
                        "created_at": created_at.isoformat(),
                    },
                }
            ),
            201,
        )

    except Exception as e:
        logger.error(f"Error rating recipe: {str(e)}", exc_info=True)
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500


@rating_controller.route("/user-rating/<int:recipe_id>", methods=["GET"])
@token_required
def get_user_rating(current_user, recipe_id):
    try:
        logger.info(f"Getting rating for recipe {recipe_id} by user {current_user.user_id}")

        result = db.session.execute(
            text(
                """
                SELECT rating, created_at 
                FROM rating 
                WHERE user_id = :user_id AND recipe_id = :recipe_id
            """
            ),
            {"user_id": current_user.user_id, "recipe_id": recipe_id},
        ).first()

        if result:
            return jsonify(
                {
                    "status": "success",
                    "data": {
                        "rating": result.rating,
                        "created_at": result.created_at.isoformat() if result.created_at else None,
                    },
                }
            )
        return jsonify({"status": "success", "data": None})

    except Exception as e:
        logger.error(f"Error getting recipe rating: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500
