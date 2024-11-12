# Auth/auth.py
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash
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

    
    
@bp_auth.route('/login',methods=['POST'])
def login():
    data=request.get_json()
    username=data.get('username')
