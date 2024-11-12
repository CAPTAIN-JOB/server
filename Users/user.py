from flask import Blueprint,jsonify

from models import User


users_bp = Blueprint('user', __name__)

@users_bp.route('/users')
def index():
    users = User.query.all()
    return  jsonify([user.to_dict() for user in users]) 



