import logging
from datetime import datetime, timedelta

from config.database import db
from flask import Blueprint, jsonify, request
from models.nutrition import Nutrition
from models.user import User
from sqlalchemy.sql import text
from utils.auth import token_required

logger = logging.getLogger(__name__)

user_nutrition_controller = Blueprint("user_nutrition_controller", __name__)


@user_nutrition_controller.route("/nutrition/daily", methods=["GET"])
@token_required
def get_daily_nutrition(current_user):
    """Get user's daily nutrition intake and recommendations"""
    try:
        # Get user's age group and today's nutrition intake
        query = """
            WITH DailyNutrition AS (
                SELECT 
                    n.name as nutrition_name,
                    n.unit,
                    COALESCE(SUM(c.amount), 0) as consumed_amount
                FROM nutrition n
                LEFT JOIN contains c ON n.name = c.nutrition_name
                LEFT JOIN eats e ON c.recipe_id = e.recipe_id
                    AND e.user_id = :user_id
                    AND DATE(e.created_at) = CURDATE()
                GROUP BY n.name, n.unit
            )
            SELECT 
                dn.nutrition_name,
                dn.unit,
                dn.consumed_amount,
                npa.recommended_daily_value,
                ROUND(
                    (dn.consumed_amount / npa.recommended_daily_value) * 100, 
                    1
                ) as percentage_fulfilled
            FROM DailyNutrition dn
            JOIN user_age_group uag ON uag.user_id = :user_id
            JOIN user u ON u.user_id = :user_id
            JOIN nutrition_per_age npa ON 
                npa.age_group = uag.age_group 
                AND npa.sex = u.sex
                AND npa.nutrition_name = dn.nutrition_name
            ORDER BY dn.nutrition_name
        """

        result = db.session.execute(text(query), {"user_id": current_user.user_id})

        nutrition_data = [
            {
                "name": row.nutrition_name,
                "unit": row.unit,
                "consumed": float(row.consumed_amount),
                "recommended": float(row.recommended_daily_value),
                "percentageFulfilled": float(row.percentage_fulfilled),
            }
            for row in result
        ]

        return jsonify({"status": "success", "data": nutrition_data})
    except Exception as e:
        logger.error(f"Error getting daily nutrition: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@user_nutrition_controller.route("/nutrition/weekly", methods=["GET"])
@token_required
def get_weekly_nutrition(current_user):
    """Get user's weekly nutrition intake and recommendations"""
    try:
        query = """
            WITH WeeklyNutrition AS (
                SELECT 
                    n.name as nutrition_name,
                    n.unit,
                    DATE(e.created_at) as consumption_date,
                    COALESCE(SUM(c.amount), 0) as daily_amount
                FROM nutrition n
                LEFT JOIN contains c ON n.name = c.nutrition_name
                LEFT JOIN eats e ON c.recipe_id = e.recipe_id
                    AND e.user_id = :user_id
                    AND e.created_at >= DATE_SUB(CURDATE(), INTERVAL 7 DAY)
                GROUP BY n.name, n.unit, DATE(e.created_at)
            )
            SELECT 
                wn.nutrition_name,
                wn.unit,
                wn.consumption_date,
                wn.daily_amount as consumed_amount,
                npa.recommended_daily_value,
                ROUND(
                    (wn.daily_amount / npa.recommended_daily_value) * 100, 
                    1
                ) as percentage_fulfilled
            FROM WeeklyNutrition wn
            JOIN user_age_group uag ON uag.user_id = :user_id
            JOIN user u ON u.user_id = :user_id
            JOIN nutrition_per_age npa ON 
                npa.age_group = uag.age_group 
                AND npa.sex = u.sex
                AND npa.nutrition_name = wn.nutrition_name
            WHERE wn.consumption_date IS NOT NULL
            ORDER BY wn.consumption_date DESC, wn.nutrition_name
        """

        result = db.session.execute(text(query), {"user_id": current_user.user_id})

        # Group by date
        nutrition_data = {}
        for row in result:
            date_str = row.consumption_date.strftime("%Y-%m-%d")
            if date_str not in nutrition_data:
                nutrition_data[date_str] = []

            nutrition_data[date_str].append(
                {
                    "name": row.nutrition_name,
                    "unit": row.unit,
                    "consumed": float(row.consumed_amount),
                    "recommended": float(row.recommended_daily_value),
                    "percentageFulfilled": float(row.percentage_fulfilled),
                }
            )

        return jsonify({"status": "success", "data": nutrition_data})
    except Exception as e:
        logger.error(f"Error getting weekly nutrition: {str(e)}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500
