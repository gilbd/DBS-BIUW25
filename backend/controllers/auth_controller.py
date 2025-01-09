from flask import Blueprint, request, jsonify
from werkzeug.security import check_password_hash
from models.user import User
from models.admin import Admin
import jwt
import datetime
from config.settings import SECRET_KEY

auth_controller = Blueprint("auth_controller", __name__)


@auth_controller.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    # Check if we're using email or user_id for login
    if "email" in data:
        user = User.query.filter_by(email=data["email"]).first()
    elif "userId" in data:
        user = User.query.get(data["userId"])
    else:
        return jsonify({"error": "Email or User ID is required"}), 400

    if not user:
        return jsonify({"error": "User not found"}), 404

    if not check_password_hash(user.password_hash, data["password"]):
        return jsonify({"error": "Invalid password"}), 401

    # Check if user is admin
    is_admin = Admin.query.filter_by(user_id=user.user_id).first() is not None

    # Generate token
    token = jwt.encode(
        {
            "user_id": user.user_id,
            "email": user.email,
            "is_admin": is_admin,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
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
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        return jsonify({"error": "No token provided"}), 401

    try:
        token = auth_header.split(" ")[1]  # Bearer <token>
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        user = User.query.get(payload["user_id"])
        if not user:
            return jsonify({"error": "User not found"}), 404

        is_admin = Admin.query.filter_by(user_id=user.user_id).first() is not None

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
