from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

import hashlib
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)

# Helper function to hash passwords using hashlib
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# USER ENDPOINTS

@api.route('/users', methods=['GET'])
def get_users():
    all_users = User.query.all()
    all_users_list = list(map(lambda user: user.serialize(), all_users))
    return jsonify(all_users_list), 200

@api.route('/signup', methods=['POST'])
def signup():
    user_data = request.json
    required_properties = ["email", "password"]

    for prop in required_properties:
        if prop not in user_data:
            return jsonify({"error": f"The property '{prop}' was not properly written"}), 400 

    for key in user_data:
        if user_data[key] == "":
            return jsonify({"error": f"The '{key}' must not be empty"}), 400 

    # Hash the password before storing it
    user_data['password'] = hash_password(user_data['password'])

    user_to_add = User(**user_data)
    db.session.add(user_to_add)
    db.session.commit()

    return jsonify(user_to_add.serialize()), 200

@api.route("/login", methods=["POST"])
def login():
    user_data = request.json
    required_properties = ["email", "password"]

    for prop in required_properties:
        if prop not in user_data:
            return jsonify({"error": f"The '{prop}' property of the user is not or is not properly written"}), 400

    user = User.query.filter_by(email=user_data["email"]).first()

    # Check if user exists and password is correct
    if user is None or user.password != hash_password(user_data['password']):
        return jsonify({"error": "Bad username or password"}), 401

    access_token = create_access_token(identity=user_data["email"])
    return jsonify(access_token=access_token)

@api.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(valid=bool(current_user)), 200

@api.route('/users/<int:user_id>', methods=['DELETE'])
def del_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if not user:
        return jsonify({"error": f"The ID '{user_id}' is not associated with any user"}), 400 
    db.session.delete(user)
    db.session.commit()

    return jsonify({"Deleted": f"The user '{user.email}' was deleted successfully"}), 200
