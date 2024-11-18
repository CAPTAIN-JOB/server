# Auth/auth.py
import jwt
import datetime

from flask_jwt_extended import JWTManager, create_refresh_token, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies


from flask import Blueprint, request, jsonify,current_app,make_response
from werkzeug.security import generate_password_hash,check_password_hash
from extensions import db
from models import User

bp_auth = Blueprint("auth", __name__)






@bp_auth.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    name = data.get('name')
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    if not (name and username and email and password):
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({"error": "Username or email already exists"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(name=name, username=username, email=email, password=hashed_password)

    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201



@bp_auth.route('/login', methods=['POST'])
def login():
    # Retrieve JSON data
    data = request.get_json()
    
    # Check if data exists
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400

    email = data.get('email')
    password = data.get('password')

    if not (email and password):
        return jsonify({"error": "Email and Password are required"}), 400

    user = User.query.filter_by(email=email).first()
    
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=user.id) 
        refresh_token = create_refresh_token(identity=user.id) 
        return make_response({
            'msg': 'Login successful',
            'tokens': {
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        }, 200)
         
        # return jsonify({"message": "Login successful", "token": token}), 200
    else:
        return jsonify({"error": "Invalid email or password"}), 401