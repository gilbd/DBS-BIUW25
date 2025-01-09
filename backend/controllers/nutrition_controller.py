from flask import Blueprint, request, jsonify
from app import db
from app.models.nutrition import Nutrition

nutrition_controller = Blueprint('nutrition_controller', __name__)

# Get all nutrition items
@nutrition_controller.route('/nutrition', methods=['GET'])
def get_all_nutrition():
    nutrition_items = Nutrition.query.all()
    return jsonify([nutrition.to_dict() for nutrition in nutrition_items])

# Get a single nutrition item by name
@nutrition_controller.route('/nutrition/<string:nutrition_name>', methods=['GET'])
def get_nutrition(nutrition_name):
    nutrition = Nutrition.query.get(nutrition_name)
    if nutrition:
        return jsonify(nutrition.to_dict())
    return jsonify({"error": "Nutrition item not found"}), 404

# Create a new nutrition item
@nutrition_controller.route('/nutrition', methods=['POST'])
def create_nutrition():
    name = request.json.get('name')
    description = request.json.get('description')
    
    if not name:
        return jsonify({"error": "Name is required"}), 400
    
    new_nutrition = Nutrition(name=name, description=description)
    db.session.add(new_nutrition)
    db.session.commit()
    return jsonify(new_nutrition.to_dict()), 201

# Update an existing nutrition item
@nutrition_controller.route('/nutrition/<string:nutrition_name>', methods=['PUT'])
def update_nutrition(nutrition_name):
    nutrition = Nutrition.query.get(nutrition_name)
    if not nutrition:
        return jsonify({"error": "Nutrition item not found"}), 404
    
    nutrition.description = request.json.get('description', nutrition.description)
    db.session.commit()
    return jsonify(nutrition.to_dict())

# Delete a nutrition item
@nutrition_controller.route('/nutrition/<string:nutrition_name>', methods=['DELETE'])
def delete_nutrition(nutrition_name):
    nutrition = Nutrition.query.get(nutrition_name)
    if not nutrition:
        return jsonify({"error": "Nutrition item not found"}), 404
    
    db.session.delete(nutrition)
    db.session.commit()
    return jsonify({"message": "Nutrition item deleted successfully"})