from flask import Blueprint, request, jsonify
from app import db
from app.models.admin import Admin
from app.models.user import User

admin_controller = Blueprint('admin_controller', __name__)

# Get all admins
@admin_controller.route('/admins', methods=['GET'])
def get_all_admins():
    admins = Admin.query.all()
    return jsonify([admin.to_dict() for admin in admins])

# Create a new admin
@admin_controller.route('/admins', methods=['POST'])
def create_admin():
    user_id = request.json.get('user_id')
    user = User.query.get(user_id)
    if user:
        new_admin = Admin(user_id=user_id)
        db.session.add(new_admin)
        db.session.commit()
        return jsonify(new_admin.to_dict()), 201
    return jsonify({"error": "User not found"}), 404