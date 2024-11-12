from flask import Blueprint,current_app,jsonify,request
from extensions import db
from models import Pay

mpesa_bp = Blueprint('mpesa', __name__)


@mpesa_bp.route('/donate',methods=['POST'])
def pay():
    data = request.get_json()
    phone_number = data.get('phone_number')
    amount = data.get('amount')
    response = lipa_na_mpesa_online(amount,phone_number) 
    
    return



@bp_callback.route('/callback', methods=['POST'])
def mpesa_callback():
    data = request.json
    # Process callback data
    return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})


