from config.database import db
from flask import Blueprint, jsonify, request
from models.diet import Diet

diet_controller = Blueprint("diet_controller", __name__)


# Get all diets
@diet_controller.route("/", methods=["GET"])
def get_all_diets():
    diets = Diet.query.all()
    return jsonify([diet.to_dict() for diet in diets])


# Get a single diet by ID
@diet_controller.route("/<int:diet_id>", methods=["GET"])
def get_diet(diet_id):
    diet = Diet.query.get(diet_id)
    if diet:
        return jsonify(diet.to_dict())
    return jsonify({"error": "Diet not found"}), 404


# Create a new diet
@diet_controller.route("", methods=["POST"])
def create_diet():
    name = request.json.get("name")
    keywords = request.json.get("keywords")
    description = request.json.get("description")

    if not name:
        return jsonify({"error": "Name is required"}), 400

    new_diet = Diet(name=name, keywords=keywords, description=description)
    db.session.add(new_diet)
    db.session.commit()
    return jsonify(new_diet.to_dict()), 201


# Update an existing diet
@diet_controller.route("/<int:diet_id>", methods=["PUT"])
def update_diet(diet_id):
    diet = Diet.query.get(diet_id)
    if not diet:
        return jsonify({"error": "Diet not found"}), 404

    diet.name = request.json.get("name", diet.name)
    diet.keywords = request.json.get("keywords", diet.keywords)
    diet.description = request.json.get("description", diet.description)

    db.session.commit()
    return jsonify(diet.to_dict())


# Delete a diet
@diet_controller.route("/<int:diet_id>", methods=["DELETE"])
def delete_diet(diet_id):
    diet = Diet.query.get(diet_id)
    if not diet:
        return jsonify({"error": "Diet not found"}), 404

    db.session.delete(diet)
    db.session.commit()
    return jsonify({"message": "Diet deleted successfully"})
