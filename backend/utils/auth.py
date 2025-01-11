from functools import wraps

import jwt
from config.database import db
from config.settings import SECRET_KEY
from flask import jsonify, request
from models.admin import Admin
from models.user import User
from sqlalchemy.sql import text


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")

        if auth_header:
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({"error": "Invalid token format"}), 401

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            result = db.session.execute(
                text("SELECT * FROM user WHERE user_id = :user_id"), {"user_id": data["user_id"]}
            ).first()
            current_user = User.query.get(result) if result else None
            if not current_user:
                return jsonify({"error": "User not found"}), 404
        except:
            return jsonify({"error": "Invalid token"}), 401

        return f(current_user, *args, **kwargs)

    return decorated


def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        auth_header = request.headers.get("Authorization")

        if auth_header:
            try:
                token = auth_header.split(" ")[1]
            except IndexError:
                return jsonify({"error": "Invalid token format"}), 401

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            # Get user
            result = db.session.execute(
                text("SELECT * FROM user WHERE user_id = :user_id"), {"user_id": data["user_id"]}
            ).first()
            current_user = User.query.get(result) if result else None

            if not current_user:
                return jsonify({"error": "User not found"}), 404

            # Check if user is admin
            admin_result = db.session.execute(
                text("SELECT * FROM admin WHERE user_id = :user_id"),
                {"user_id": current_user.user_id},
            ).first()

            if not admin_result:
                return jsonify({"error": "Admin privileges required"}), 403
        except:
            return jsonify({"error": "Invalid token"}), 401

        return f(current_user, *args, **kwargs)

    return decorated
