# from flask import Blueprint,current_app,jsonify,request
# from extensions import db
# from Mpesa.services import lipa_na_mpesa_online
# from models import Pay

# mpesa_bp = Blueprint('mpesa', __name__)
# bp_callback =Blueprint('callback', __name__)


# @mpesa_bp.route('/donate',methods=['POST'])
# def pay():
#     data = request.get_json()
#     phone_number = data.get('phone_number')
#     amount = data.get('amount')
#     response = lipa_na_mpesa_online(amount,phone_number) 
    
#     return jsonify(response),200



# @bp_callback.route('/callback', methods=['POST'])
# def mpesa_callback():
#     data = request.json
#     print("MPESA Callback Data:", data)
#     # Process callback data
#     return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"}),200


