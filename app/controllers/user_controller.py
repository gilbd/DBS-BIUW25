from flask import Blueprint, request, jsonify
from app import db
from app.models.user import User

user_controller = Blueprint('user_controller', __name__)

# Create new user
@user_controller.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    new_user = User(
        name=data['name'],
        date_of_birth=data['date_of_birth'],
        weight=data['weight'],
        height=data['height'],
        sex=data['sex'],
        email=data['email'],
        password_hash=data['password_hash']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

# Get user according id
@user_controller.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    user = User.query.get(id)
    if user:
        return jsonify(user.to_dict()), 200
    return jsonify({'message': 'User not found'}), 404


# Delete User according id
@user_controller.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get(id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': 'User deleted'}), 200
    return jsonify({'message': 'User not found'}), 404

# Update User according id
@user_controller.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get(id)
    if user:
        user.name = data.get('name', user.name)
        user.date_of_birth = data.get('date_of_birth', user.date_of_birth)
        user.weight = data.get('weight', user.weight)
        user.height = data.get('height', user.height)
        user.sex = data.get('sex', user.sex)
        user.email = data.get('email', user.email)
        user.password_hash = data.get('password_hash', user.password_hash)
        db.session.commit()
        return jsonify(user.to_dict()), 200
    return jsonify({'message': 'User not found'}), 404