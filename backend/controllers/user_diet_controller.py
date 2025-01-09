from config.database import db
from flask import Blueprint, jsonify, request
from models.diet import Diet
from models.relationships.user_diet import UserDiet
from models.user import User

user_diet_controller = Blueprint("user_diet_controller", __name__)


# Assign a diet to a user
@user_diet_controller.route("/user_diets", methods=["POST"])
def add_user_diet():
    user_id = request.json.get("user_id")
    diet_id = request.json.get("diet_id")

    user = User.query.get(user_id)
    diet = Diet.query.get(diet_id)

    if user and diet:
        user_diet = UserDiet(user_id=user_id, diet_id=diet_id)
        db.session.add(user_diet)
        db.session.commit()
        return jsonify(user_diet.to_dict()), 201
    return jsonify({"error": "User or Diet not found"}), 404
