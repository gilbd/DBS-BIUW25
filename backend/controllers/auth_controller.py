import logging
from datetime import datetime, timedelta, timezone
from typing import Optional, TypedDict

import bcrypt
import jwt
from config.database import db
from config.settings import SECRET_KEY
from flask import Blueprint, jsonify, request
from models.admin import Admin
from models.user import User
from sqlalchemy.sql import text

logger = logging.getLogger(__name__)


class LoginRequest(TypedDict, total=False):
    email: Optional[str]
    userId: Optional[int]
    password: str


auth_controller = Blueprint("auth_controller", __name__)


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


@auth_controller.route("/login", methods=["POST"])
def login():
    data: LoginRequest = request.get_json()
    logger.info(f"Login attempt with data: {data}")

    try:
        # Check if we're using email or user_id for login
        if "email" in data:
            result = db.session.execute(
                text(
                    """
                    SELECT u.*, uag.age_group 
                    FROM user u 
                    LEFT JOIN user_age_group uag ON u.user_id = uag.user_id 
                    WHERE u.email = :email
                """
                ),
                {"email": data["email"]},
            ).first()
        elif "userId" in data:
            result = db.session.execute(
                text(
                    """
                    SELECT u.*, uag.age_group 
                    FROM user u 
                    LEFT JOIN user_age_group uag ON u.user_id = uag.user_id 
                    WHERE u.user_id = :user_id
                """
                ),
                {"user_id": data["userId"]},
            ).first()
        else:
            return jsonify({"error": "Email or User ID is required"}), 400

        if not result:
            return jsonify({"error": "User not found"}), 404

        if not bcrypt.checkpw(
            data["password"].encode("utf-8"), result.password_hash.encode("utf-8")
        ):
            return jsonify({"error": "Invalid password"}), 401

        # Check if user is admin
        admin_result = db.session.execute(
            text("SELECT * FROM admin WHERE user_id = :user_id"),
            {"user_id": result.user_id},
        ).first()
        is_admin = admin_result is not None

        # Update age group if needed
        if not result.age_group:
            age_group = calculate_age_group(result.date_of_birth)
            db.session.execute(
                text(
                    """
                    INSERT INTO user_age_group (user_id, age_group) 
                    VALUES (:user_id, :age_group)
                    ON DUPLICATE KEY UPDATE age_group = :age_group
                """
                ),
                {"user_id": result.user_id, "age_group": age_group},
            )
            db.session.commit()

        # Generate token with expiration
        expiration = datetime.now() + timedelta(hours=24)
        token = jwt.encode(
            {
                "user_id": result.user_id,
                "email": result.email,
                "is_admin": is_admin,
                "exp": expiration.timestamp(),  # Use timestamp instead of datetime
            },
            SECRET_KEY,
            algorithm="HS256",
        )

        return jsonify(
            {
                "token": token,
                "user": {
                    "user_id": result.user_id,
                    "name": result.name,
                    "email": result.email,
                    "isAdmin": is_admin,
                    "age_group": result.age_group or calculate_age_group(result.date_of_birth),
                },
            }
        )
    except Exception as e:
        logger.error(f"Login error: {str(e)}", exc_info=True)
        return jsonify({"error": "An error occurred during login"}), 500


@auth_controller.route("/verify", methods=["GET"])
def verify_token():
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "No token provided"}), 401

    try:
        token = auth_header.split(" ")[1]  # Bearer <token>
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        result = db.session.execute(
            text(
                """
                SELECT u.*, uag.age_group 
                FROM user u 
                LEFT JOIN user_age_group uag ON u.user_id = uag.user_id 
                WHERE u.user_id = :user_id
            """
            ),
            {"user_id": payload["user_id"]},
        ).first()

        if not result:
            return jsonify({"error": "User not found"}), 404

        # Check if user is admin
        admin_result = db.session.execute(
            text("SELECT * FROM admin WHERE user_id = :user_id"),
            {"user_id": result.user_id},
        ).first()
        is_admin = admin_result is not None

        return jsonify(
            {
                "user": {
                    "user_id": result.user_id,
                    "name": result.name,
                    "email": result.email,
                    "isAdmin": is_admin,
                    "age_group": result.age_group or calculate_age_group(result.date_of_birth),
                }
            }
        )
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        logger.error(f"Token verification error: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500
