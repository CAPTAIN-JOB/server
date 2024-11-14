# app.py
from flask import Flask, jsonify, request,make_response
import base64
import requests
from flask_jwt_extended import JWTManager, create_refresh_token, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from extensions import db, migrate
from Auth.auth import bp_auth
from datetime import datetime
# from Mpesa.mpesa import mpesa_bp
# from Mpesa.mpesa import bp_callback
from models import *
from dotenv import load_dotenv
import os

def create_app():

    load_dotenv()
    
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("URL_DB")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
    app.config["CALLBACK_URL"] = os.getenv("CALLBACK_URL")
    app.config["CONSUMER_KEY"] = os.getenv("CONSUMER_KEY")
    app.config["CONSUMER_SECRET"] = os.getenv("CONSUMER_SECRET")

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)

    # Register blueprints
    app.register_blueprint(bp_auth, url_prefix='/auth')
    # app.register_blueprint(bp_auth)
    # app.register_blueprint(mpesa_bp, url_prifix = '/pay')
    # app.register_blueprint(bp_callback)
    

 

 
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none() 

# JWT error handling
    @jwt.expired_token_loader
    def jwt_expired_token(jwt_header, jwt_data):
        return make_response({'message': "Token has expired", "error": "token_expired"}, 401)

    @jwt.invalid_token_loader
    def jwt_invalid_token(error):
        return make_response({'message': 'Invalid token', "error": "invalid_token"}, 401)

    @jwt.unauthorized_loader
    def missing_token(error):
        return make_response({'message': 'Missing token', "error": "missing_token"}, 401)

    @jwt.token_in_blocklist_loader
    def token_in_blocklist(jwt_header, jwt_data):
        jti = jwt_data['jti']
        token = db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()
        return token is not None
    
  
  
  
  
  
    # Function to generate the MPESA access token
    def get_access_token():
        consumer_key = app.config['CONSUMER_KEY']
        consumer_secret = app.config['CONSUMER_SECRET']
        auth_url = f"{app.config['MPESA_API_URL']}/oauth/v1/generate?grant_type=client_credentials"

        response = requests.get(auth_url, auth=(consumer_key, consumer_secret))
        if response.status_code == 200:
            return response.json().get('access_token')
        else:
            return None
  
  
    # init payment
    def lipa_na_mpesa(amount,phone_number):
        access_token = get_access_token
        
        if not access_token:
            return {"error": "Unable to generate access token"}
        
        # timestamp = datetime.datetime.now()strftime("%Y%m%d%H%M%S")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode(
            f"{app.config['MPESA_SHORTCODE']}{app.config['MPESA_PASSKEY']}{timestamp}".encode()
        ).decode('utf-8')
        
        
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }
    
        payload = {
            "BusinessShortCode": app.config['MPESA_SHORTCODE'],
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": "0748292218",
            "PartyB": app.config['MPESA_SHORTCODE'],
            "PhoneNumber": phone_number,
            "CallBackURL": app.config['CALLBACK_URL'],
            "AccountReference": "Donation",
            "TransactionDesc": "Charity Donation"
        }
    
        response = requests.post(
            f"{app.config['MPESA_API_URL']}/mpesa/stkpush/v1/processrequest",
            json=payload,
            headers=headers
        )
        
        return response.json()
    
        
    
    
    
 
    # Events Routes

    @app.route('/')
    @jwt_required()
    def index():
        return "Welcome to the Non Communicable Diseases"
    
    
    
    @app.route('/donate' , methods=['POST'])
    @jwt_required()
    def pay():
        data = request.get_json()
        phone_number = data.get('phone_number')
        amount = data.get('amount')

        
        response = lipa_na_mpesa(amount,phone_number)

        return jsonify(response),200
        
    @app.route('/callback', methods=['POST'])
    
    def mpesa_callback():
        data = request.get_json()
        transaction_id = data.get("transaction_id")
        result_code = data.get("ResultCode")

    # Find the transaction in the database
        transaction = Transaction.query.filter_by(transaction_id=transaction_id).first()

        if not transaction:
            return jsonify({"error": "Transaction not found"}), 404

    # Update the status based on the ResultCode
        if result_code == 0:
            transaction.status = "Completed"
        else:
            transaction.status = "Failed"

        db.session.commit()

    # Respond to the Daraja API callback
        return jsonify({"ResultCode": 0, "ResultDesc": "Accepted"})
    
    
    @app.route('/events', methods=['GET'])
    @jwt_required()
    def get_events():
        events = Event.query.all()
        return jsonify([event.to_dict() for event in events]), 200


    @app.route('/events/<int:event_id>', methods=['GET'])
    def get_event(event_id):
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Event not found"}), 404
        return jsonify(event.to_dict()), 200


    @app.route('/events', methods=['POST'])
    @jwt_required()
    def create_event():

        data = request.json
        try:
            event_date = datetime.strptime(data.get('date'), "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return make_response(jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400)
        created_by_user_id = get_jwt_identity()
        if not created_by_user_id:
            return make_response(jsonify({"error": "User ID missing from token."}), 400)
        
        new_event = Event(
        title=data.get('title'),
        description=data.get('description'),
        date=event_date,
        banner=data.get('banner'),
        created_by_user_id=created_by_user_id  # Set from token
    )
 
         
        db.session.add(new_event)
        db.session.commit()
        return make_response(jsonify(new_event.to_dict())), 201
        
     


    @app.route('/events/<int:event_id>', methods=['DELETE'])
    @jwt_required()

    def delete_event(event_id):
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Event not found"}), 404
        db.session.delete(event)
        db.session.commit()
        return make_response({"message": "Event deleted successfully"}), 200


    # Diseases Routes
    @app.route('/diseases', methods=['GET'])
    @jwt_required()

    def get_diseases():
        diseases = Disease.query.all()
        return jsonify([disease.to_dict() for disease in diseases]), 200


    @app.route('/diseases/<int:disease_id>', methods=['GET'])
    @jwt_required()

    def get_disease(disease_id):
        disease = Disease.query.get(disease_id)
        if not disease:
            return jsonify({"error": "Disease not found"}), 404
        return jsonify(disease.to_dict()), 200


    @app.route('/diseases', methods=['POST'])
    @jwt_required()

    def create_disease():
        data = request.json
        new_disease = Disease(
            name=data.get('name'),
            description=data.get('description'),
            symptoms=data.get('symptoms'),
            prevention_tips=data.get('prevention_tips')
        )
        db.session.add(new_disease)
        db.session.commit()
        return make_response({'message': "Diseases added successfully"}), 201


    @app.route('/diseases/<int:disease_id>', methods=['DELETE'])
    @jwt_required()

    def delete_disease(disease_id):
        disease = Disease.query.get(disease_id)
        if not disease:
            return jsonify({"error": "Disease not found"}), 404
        db.session.delete(disease)
        db.session.commit()
        return jsonify({"message": "Disease deleted successfully"}), 200

    return app



# if __name__ == "__main__":
#     app = create_app()
#     app.run(port=5500, debug=True)
