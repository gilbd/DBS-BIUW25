from flask import Blueprint, request, jsonify
from app import db
from app.models.relationships.user_nutrition import UserNutrition
from app.models.nutrition import Nutrition
from app.models.user import User

user_nutrition_controller = Blueprint('user_nutrition_controller', __name__)

# Track nutrition for a user
@user_nutrition_controller.route('/user_nutrition', methods=['POST'])
def track_user_nutrition():
    user_id = request.json.get('user_id')
    nutrition_name = request.json.get('nutrition_name')
    tracked_value = request.json.get('tracked_value')
    
    user = User.query.get(user_id)
    nutrition = Nutrition.query.get(nutrition_name)
    
    if user and nutrition:
        user_nutrition = UserNutrition(user_id=user_id, nutrition_name=nutrition_name, tracked_value=tracked_value)
        db.session.add(user_nutrition)
        db.session.commit()
        return jsonify(user_nutrition.to_dict()), 201
    return jsonify({"error": "User or Nutrition not found"}), 404