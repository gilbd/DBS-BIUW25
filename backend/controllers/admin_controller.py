import logging
from datetime import datetime, timedelta

from config.database import db
from flask import Blueprint, jsonify, request
from models.admin import Admin
from models.user import User
from sqlalchemy.sql import text
from utils.auth import admin_required

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

admin_controller = Blueprint("admin_controller", __name__)


# Get all admins
@admin_controller.route("/admins", methods=["GET"])
def get_all_admins():
    result = db.session.execute(text("SELECT * FROM admin")).fetchall()
    admins = [Admin.query.get(admin[0]) for admin in result]
    return jsonify([admin.to_dict() for admin in admins])


# Create a new admin
@admin_controller.route("/admins", methods=["POST"])
def create_admin():
    user_id = request.json.get("user_id")
    result = db.session.execute(
        text("SELECT * FROM user WHERE user_id = :user_id"), {"user_id": user_id}
    ).first()
    user = User.query.get(result[0]) if result else None
    if user:
        db.session.execute(
            text("INSERT INTO admin (user_id) VALUES (:user_id)"), {"user_id": user_id}
        )
        db.session.commit()
        result = db.session.execute(
            text("SELECT * FROM admin WHERE user_id = :user_id"), {"user_id": user_id}
        ).first()
        admin = Admin.query.get(result[0])
        return jsonify(admin.to_dict()), 201
    return jsonify({"error": "User not found"}), 404


@admin_controller.route("/stats/weekly", methods=["GET"])
@admin_required
def get_weekly_stats(current_user):
    try:
        logger.info(f"Getting weekly stats for admin user: {current_user.user_id}")

        # Get eats count for each day in the last week
        query = """
            SELECT 
                DATE(created_at) as day,
                COUNT(*) as eats
            FROM eats
            WHERE created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            GROUP BY DATE(created_at)
            ORDER BY day;
        """
        logger.info(f"Executing query: {query}")
        result = db.session.execute(text(query))
        weekly_stats = [{"day": row.day.strftime("%a"), "eats": row.eats} for row in result]
        logger.info(f"Weekly stats results: {weekly_stats}")

        return jsonify({"status": "success", "data": weekly_stats})
    except Exception as e:
        logger.error(f"Error in get_weekly_stats: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@admin_controller.route("/stats/top-recipes", methods=["GET"])
@admin_required
def get_top_recipes(current_user):
    try:
        logger.info(f"Getting top recipes for admin user: {current_user.user_id}")

        query = """
            SELECT 
                r.recipe_name,
                COUNT(*) as eats
            FROM eats e
            JOIN recipe r ON e.recipe_id = r.recipe_id
            WHERE e.created_at >= DATE_SUB(CURDATE(), INTERVAL 30 DAY)
            GROUP BY r.recipe_id, r.recipe_name
            ORDER BY eats DESC
            LIMIT 5;
        """
        logger.info(f"Executing query: {query}")
        result = db.session.execute(text(query))
        top_recipes = [{"name": row.recipe_name, "eats": row.eats} for row in result]
        logger.info(f"Top recipes results: {top_recipes}")

        return jsonify({"status": "success", "data": top_recipes})
    except Exception as e:
        logger.error(f"Error in get_top_recipes: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@admin_controller.route("/stats/diet-violations", methods=["GET"])
@admin_required
def get_diet_violations(current_user):
    try:
        logger.info(f"Getting diet violations for admin user: {current_user.user_id}")

        query = """
            SELECT 
                u.user_id,
                u.name as user_name,
                r.recipe_name,
                d.name as diet_name,
                e.created_at as violation_date
            FROM eats e
            JOIN user u ON e.user_id = u.user_id 
            JOIN recipe r ON e.recipe_id = r.recipe_id
            JOIN user_diet ud ON u.user_id = ud.user_id
            JOIN diet d ON ud.diet_id = d.diet_id
            WHERE NOT EXISTS (
                SELECT 1 FROM fits f 
                WHERE f.recipe_id = e.recipe_id 
                AND f.diet_id = ud.diet_id
            )
            AND e.created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
            ORDER BY e.created_at DESC
            LIMIT 10;
        """
        logger.info(f"Executing query: {query}")
        result = db.session.execute(text(query))
        violations = [
            {
                "userId": row.user_id,
                "user": row.user_name,
                "recipe": row.recipe_name,
                "diet": row.diet_name,
            }
            for row in result
        ]
        logger.info(f"Diet violations results: {violations}")

        return jsonify({"status": "success", "data": violations})
    except Exception as e:
        logger.error(f"Error in get_diet_violations: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@admin_controller.route("/stats/calorie-violations", methods=["GET"])
@admin_required
def get_calorie_violations(current_user):
    try:
        logger.info(f"Getting calorie violations for admin user: {current_user.user_id}")

        query = """
            WITH UserDailyCalories AS (
                SELECT 
                    u.user_id,
                    u.name as user_name,
                    uag.age_group,
                    u.sex,
                    DATE(e.created_at) as eat_date,
                    SUM(c.amount) as daily_calories,
                    npa.recommended_daily_value as recommended_calories
                FROM eats e
                JOIN user u ON e.user_id = u.user_id
                JOIN recipe r ON e.recipe_id = r.recipe_id
                JOIN contains c ON r.recipe_id = c.recipe_id
                JOIN nutrition n ON c.nutrition_name = n.name
                JOIN user_age_group uag ON u.user_id = uag.user_id
                JOIN nutrition_per_age npa ON (
                    uag.age_group = npa.age_group 
                    AND u.sex = npa.sex 
                    AND n.name = npa.nutrition_name
                )
                WHERE 
                    n.name = 'Calories'
                    AND e.created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                GROUP BY 
                    u.user_id, u.name, uag.age_group, u.sex, 
                    DATE(e.created_at), npa.recommended_daily_value
            )
            SELECT 
                user_id,
                user_name,
                age_group,
                sex,
                ROUND(AVG(daily_calories), 2) as avg_daily_calories,
                recommended_calories,
                ROUND(
                    (AVG(daily_calories) - recommended_calories) 
                    / recommended_calories * 100, 
                    1
                ) as excess_percentage
            FROM UserDailyCalories
            GROUP BY 
                user_id, user_name, age_group, sex, recommended_calories
            HAVING AVG(daily_calories) > (recommended_calories * 1.4)
            ORDER BY excess_percentage DESC
            LIMIT 10;
        """
        logger.info(f"Executing query: {query}")
        result = db.session.execute(text(query))
        violations = [
            {
                "userId": row.user_id,
                "user": row.user_name,
                "ageGroup": row.age_group,
                "sex": row.sex,
                "avgCalories": row.avg_daily_calories,
                "recommended": row.recommended_calories,
                "excessPercentage": row.excess_percentage,
            }
            for row in result
        ]
        logger.info(f"Calorie violations results: {violations}")

        return jsonify({"status": "success", "data": violations})
    except Exception as e:
        logger.error(f"Error in get_calorie_violations: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@admin_controller.route("/stats/top-rated", methods=["GET"])
@admin_required
def get_top_rated(current_user):
    try:
        period = request.args.get("period", "all")  # 'week' or 'all'
        logger.info(f"Getting top rated recipes for period: {period}")

        time_filter = (
            "AND rt.created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)" if period == "week" else ""
        )

        query = f"""
            SELECT 
                r.recipe_id,
                r.recipe_name,
                ROUND(AVG(rt.rating), 2) as avg_rating,
                COUNT(rt.rating) as rating_count
            FROM recipe r
            LEFT JOIN rating rt ON r.recipe_id = rt.recipe_id
            WHERE rt.rating IS NOT NULL
            {time_filter}
            GROUP BY r.recipe_id, r.recipe_name
            HAVING rating_count >= 3  -- Minimum ratings threshold
            ORDER BY avg_rating DESC, rating_count DESC
            LIMIT 10;
        """

        logger.info(f"Executing query: {query}")
        result = db.session.execute(text(query))
        top_rated = [
            {
                "recipeId": row.recipe_id,
                "recipeName": row.recipe_name,
                "avgRating": float(row.avg_rating),
                "ratingCount": row.rating_count,
            }
            for row in result
        ]
        logger.info(f"Top rated results: {top_rated}")

        return jsonify({"status": "success", "data": top_rated})
    except Exception as e:
        logger.error(f"Error in get_top_rated: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500
