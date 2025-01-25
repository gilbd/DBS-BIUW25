import logging
from datetime import datetime, timezone

from config.database import db
from flask import Blueprint, jsonify, request
from models.recipe import Recipe
from models.user import User
from sqlalchemy.sql import text

logger = logging.getLogger(__name__)

eats_controller = Blueprint("eats_controller", __name__)


@eats_controller.route("/eats", methods=["POST"])
def log_user_eats():
    try:
        data = request.get_json()
        logger.info(f"Logging user eats\n{data}")

        # Validate input
        user_id = data.get("user_id")
        recipe_id = data.get("recipe_id")

        if not user_id or not recipe_id:
            return jsonify({"error": "Missing user_id or recipe_id"}), 400

        # Check if user and recipe exist
        user = User.query.get(user_id)
        recipe = Recipe.query.get(recipe_id)

        if not user or not recipe:
            return jsonify({"error": "User or Recipe not found"}), 404

        # Create new eats record using literal query
        created_at = datetime.now(timezone.utc)
        query = """
            INSERT INTO eats (user_id, recipe_id, created_at)
            VALUES (:user_id, :recipe_id, :created_at)
        """
        db.session.execute(
            text(query), {"user_id": user_id, "recipe_id": recipe_id, "created_at": created_at}
        )
        db.session.commit()

        # Return response with data
        response_data = {
            "status": "success",
            "data": {
                "user_id": user_id,
                "recipe_id": recipe_id,
                "created_at": created_at.isoformat(),
            },
        }

        return jsonify(response_data), 201

    except Exception as e:
        logger.error(f"Error logging user eats: {str(e)}", exc_info=True)
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500
