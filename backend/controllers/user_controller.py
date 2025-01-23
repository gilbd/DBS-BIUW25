import logging
from datetime import datetime

from config.database import db
from flask import Blueprint, jsonify, request
from models.user import User
from sqlalchemy.sql import text
from utils.auth import token_required

logger = logging.getLogger(__name__)

user_controller = Blueprint("user_controller", __name__)


# Create new user
@user_controller.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(
        name=data["name"],
        date_of_birth=data["date_of_birth"],
        weight=data["weight"],
        height=data["height"],
        sex=data["sex"],
        email=data["email"],
        password_hash=data["password_hash"],
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201


# Get user according id
@user_controller.route("/users/<int:id>", methods=["GET"])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({"message": "User not found"}), 404


# Delete User according id
@user_controller.route("/users/<int:id>", methods=["DELETE"])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"message": "User not found"}), 404


# Update User according id
@user_controller.route("/users/<int:id>", methods=["PUT"])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if user:
        user.name = data.get("name", user.name)
        user.date_of_birth = data.get("date_of_birth", user.date_of_birth)
        user.weight = data.get("weight", user.weight)
        user.height = data.get("height", user.height)
        user.sex = data.get("sex", user.sex)
        user.email = data.get("email", user.email)
        user.password_hash = data.get("password_hash", user.password_hash)
        db.session.commit()
        return jsonify(user.to_dict()), 200
    return jsonify({"message": "User not found"}), 404


def calculate_age_group(date_of_birth):
    today = datetime.now()
    age = (
        today.year
        - date_of_birth.year
        - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
    )

    if age < 4:
        return "0-3"
    elif age < 9:
        return "4-8"
    elif age < 14:
        return "9-13"
    elif age < 19:
        return "14-18"
    elif age < 31:
        return "19-30"
    elif age < 51:
        return "31-50"
    else:
        return "51+"


@user_controller.route("/profile", methods=["GET"])
@token_required
def get_profile(current_user):
    try:
        result = db.session.execute(
            text(
                """
                SELECT u.*, uag.age_group 
                FROM user u 
                LEFT JOIN user_age_group uag ON u.user_id = uag.user_id 
                WHERE u.user_id = :user_id
            """
            ),
            {"user_id": current_user.user_id},
        ).first()

        if not result:
            return jsonify({"error": "User not found"}), 404

        return jsonify(
            {
                "user_id": result.user_id,
                "name": result.name,
                "email": result.email,
                "date_of_birth": result.date_of_birth.isoformat(),
                "weight": result.weight,
                "height": result.height,
                "sex": result.sex,
                "age_group": result.age_group or calculate_age_group(result.date_of_birth),
            }
        )
    except Exception as e:
        logger.error(f"Error getting profile: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500


@user_controller.route("/profile", methods=["PUT"])
@token_required
def update_profile(current_user):
    try:
        data = request.get_json()

        # Update user table
        update_query = """
            UPDATE user 
            SET name = :name,
                email = :email,
                date_of_birth = :date_of_birth,
                weight = :weight,
                height = :height,
                sex = :sex
            WHERE user_id = :user_id
        """
        db.session.execute(
            text(update_query),
            {
                "user_id": current_user.user_id,
                "name": data["name"],
                "email": data["email"],
                "date_of_birth": data["date_of_birth"],
                "weight": data["weight"],
                "height": data["height"],
                "sex": data["sex"],
            },
        )

        # Update age group
        age_group = calculate_age_group(datetime.strptime(data["date_of_birth"], "%Y-%m-%d"))
        db.session.execute(
            text(
                """
                INSERT INTO user_age_group (user_id, age_group) 
                VALUES (:user_id, :age_group)
                ON DUPLICATE KEY UPDATE age_group = :age_group
            """
            ),
            {"user_id": current_user.user_id, "age_group": age_group},
        )

        db.session.commit()
        return jsonify({"message": "Profile updated successfully"})
    except Exception as e:
        logger.error(f"Error updating profile: {str(e)}", exc_info=True)
        db.session.rollback()
        return jsonify({"error": str(e)}), 500
