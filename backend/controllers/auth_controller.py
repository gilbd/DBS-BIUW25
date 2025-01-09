import datetime
from typing import Optional, TypedDict

import bcrypt
import jwt
from config.database import db
from config.settings import SECRET_KEY
from flask import Blueprint, jsonify, request
from models.admin import Admin
from models.user import User
from sqlalchemy.sql import text


class LoginRequest(TypedDict, total=False):
    email: Optional[str]
    userId: Optional[int]
    password: str


auth_controller = Blueprint("auth_controller", __name__)


@auth_controller.route("/login", methods=["POST"])
def login():
    data: LoginRequest = request.get_json()
    print(f"Auth controller: {data}")

    # Check if we're using email or user_id for login
    if "email" in data:
        data = data["email"]
        result = db.session.execute(
            text("SELECT * FROM user WHERE email = :email"), {"email": data["email"]}
        ).first()

        user = User.query.get(result[0]) if result else None
    elif "userId" in data:
        data = data["userId"]
        result = db.session.execute(
            text("SELECT * FROM user WHERE user_id = :user_id"),
            user_id=data["userId"],
        ).first()
        user = User.query.get(result[0]) if result else None
    else:
        return jsonify({"error": "Email or User ID is required"}), 400

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not bcrypt.checkpw(data["password"].encode("utf-8"), user.password_hash.encode("utf-8")):
        return jsonify({"error": "Invalid password"}), 401

    # Check if user is admin
    admin_result = db.session.execute(
        text("SELECT * FROM admin WHERE user_id = :user_id"),
        {"user_id": user.user_id},
    ).first()
    is_admin = admin_result is not None

    # Generate token
    token = jwt.encode(
        {
            "user_id": user.user_id,
            "email": user.email,
            "is_admin": is_admin,
            "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=24),
        },
        SECRET_KEY,
        algorithm="HS256",
    )

    return jsonify(
        {
            "token": token,
            "user": {
                "user_id": user.user_id,
                "name": user.name,
                "email": user.email,
                "isAdmin": is_admin,
            },
        }
    )


@auth_controller.route("/verify", methods=["GET"])
def verify_token():
    auth_header: str | None = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "No token provided"}), 401

    try:
        token = auth_header.split(" ")[1]  # Bearer <token>
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        result = db.session.execute(
            text("SELECT * FROM user WHERE user_id = :user_id"),
            {"user_id": payload["user_id"]},
        ).first()
        user = User.query.get(result[0]) if result else None

        if not user:
            return jsonify({"error": "User not found"}), 404

        admin_result = db.session.execute(
            text("SELECT * FROM admin WHERE user_id = :user_id"),
            {"user_id": user.user_id},
        ).first()
        is_admin = admin_result is not None

        return jsonify(
            {
                "user": {
                    "user_id": user.user_id,
                    "name": user.name,
                    "email": user.email,
                    "isAdmin": is_admin,
                }
            }
        )
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
