import base64
import os
from datetime import datetime

import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, make_response, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, get_jwt_identity, jwt_required
from requests.auth import HTTPBasicAuth

from Auth.auth import bp_auth
from Auth.decorators import auth_role
from extensions import db, migrate
# from Mpesa.mpesa import mpesa_bp
# from Mpesa.mpesa import bp_callback
from models import *
from Users.user import users_bp


def create_app():

    load_dotenv()

    app = Flask(__name__)
    CORS(app)
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
    # app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("URL_DB")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["CONSUMER_KEY"] = os.getenv("CONSUMER_KEY")
    app.config["CONSUMER_SECRET"] = os.getenv("CONSUMER_SECRET")
    app.config["SHORTCODE"] = os.getenv("SHORTCODE")
    app.config["PASSKEY"] = os.getenv("PASSKEY")
    app.config["BASE_URL"] = os.getenv("BASE_URL")

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    jwt = JWTManager(app)

    # Register blueprints
    app.register_blueprint(bp_auth, url_prefix="/auth")

    app.register_blueprint(users_bp)
    # app.register_blueprint(mpesa_bp, url_prifix = '/pay')
    # app.register_blueprint(bp_callback)

    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()

    # JWT error handling
    @jwt.expired_token_loader
    def jwt_expired_token(jwt_header, jwt_data):
        return make_response(
            {"message": "Token has expired", "error": "token_expired"}, 401
        )

    @jwt.invalid_token_loader
    def jwt_invalid_token(error):
        return make_response(
            {"message": "Invalid token", "error": "invalid_token"}, 401
        )

    @jwt.unauthorized_loader
    def missing_token(error):
        return make_response(
            {"message": "Missing token", "error": "missing_token"}, 401
        )

    @jwt.token_in_blocklist_loader
    def token_in_blocklist(jwt_header, jwt_data):
        jti = jwt_data["jti"]
        token = (
            db.session.query(TokenBlocklist).filter(TokenBlocklist.jti == jti).scalar()
        )
        return token is not None

    def get_access_token():
        endpoint = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        response = requests.get(
            endpoint,
            auth=HTTPBasicAuth(
                app.config["CONSUMER_KEY"], app.config["CONSUMER_SECRET"]
            ),
        )
        return response.json().get("access_token")

    @app.route("/donate", methods=["POST"])
    @jwt_required()
    def donate():
        data = request.get_json()
        # user = data.get('name')
        amount = data.get("amount", 1)
        phone_number = data.get("phone_number")

        if not phone_number.startswith("254"):
            phone_number = "254" + phone_number[-9:]

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password_str = f"{app.config['SHORTCODE']}{app.config['PASSKEY'] }{timestamp}"
        password = base64.b64encode(password_str.encode()).decode("utf-8")

        endpoint = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
        access_token = get_access_token()
        headers = {"Authorization": f"Bearer {access_token}"}

        payload = {
            "BusinessShortCode": app.config["SHORTCODE"],
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": "0748292218",
            "PartyB": app.config["SHORTCODE"],
            "PhoneNumber": phone_number,
            "CallBackURL": app.config["BASE_URL"] + "lnmo/callback",
            "AccountReference": " Non-Communicable Diseases Charity",
            "TransactionDesc": "Charity Donation",
        }

        response = requests.post(endpoint, json=payload, headers=headers)

        response_data = response.json()

        if response_data.get("ResponseCode") == "0":
            transaction_id = response_data.get("CheckoutRequestID")

        new_transaction = Transaction(
            transaction_id=transaction_id,
            phone_number=phone_number,
            amount=amount,
            # name=user_name,  # Save user's name
            status="Pending",  # Initially set to pending
        )
        db.session.add(new_transaction)
        db.session.commit()

        return jsonify(response_data)

    @app.route("/callback", methods=["POST"])
    def mpesa_callback():
        data = request.get_json()

        # Extract the status and transaction details from the callback
        result_code = data.get("Body", {}).get("stkCallback", {}).get("ResultCode")
        transaction_id = (
            data.get("Body", {}).get("stkCallback", {}).get("CheckoutRequestID")
        )

        if result_code == 0:
            # Transaction successful
            transaction = Transaction.query.filter_by(id=transaction_id).first()
            if transaction:
                transaction.status = "Completed"
                db.session.commit()
            transaction = Transaction.query.filter_by(id=transaction_id).first()
            if transaction:
                transaction.status = "Canceled"
                db.session.commit()
        else:
            pass
        return jsonify({"ResultCode": 0, "ResultDesc": "Callback received"})

    @app.route("/transactions", methods=["GET"])
    @jwt_required()
    @auth_role("admin")
    def get_transactions():
        transactions = Transaction.query.all()
        return jsonify(
            [
                {
                    "id": tran.id,
                    "phone_number": tran.phone_number,
                    "amount": tran.amount,
                    "status": tran.status,
                    "created_at": tran.created_at,
                }
                for tran in transactions
            ]
        )

    @app.route("/events", methods=["GET"])
    # @jwt_required()

    def get_events():
        events = Event.query.all()
        return jsonify([event.to_dict() for event in events]), 200

    @app.route("/events/<int:event_id>", methods=["GET"])
    @jwt_required()

    @auth_role("admin")
    def get_event(event_id):
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Event not found"}), 404
        return jsonify(event.to_dict()), 200

    @app.route("/events", methods=["POST"])

    @jwt_required()
    @auth_role("admin")
    @auth_role("admin")
    def create_event():

        data = request.json
        try:
            event_date = datetime.strptime(data.get("date"), "%Y-%m-%d").date()
        except (ValueError, TypeError):
            return make_response(
                jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400
            )
        created_by_user_id = get_jwt_identity()
        if not created_by_user_id:
            return make_response(jsonify({"error": "User ID missing from token."}), 400)

        new_event = Event(
            title=data.get("title"),
            description=data.get("description"),
            date=event_date,
            banner=data.get("banner"),
            created_by_user_id=created_by_user_id,  # Set from token
        )

        db.session.add(new_event)
        db.session.commit()
        return make_response(jsonify(new_event.to_dict())), 201

    @app.route("/events/<int:event_id>", methods=["DELETE"])
    @jwt_required()
    @auth_role("admin")

    def delete_event(event_id):
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Event not found"}), 404
        db.session.delete(event)
        db.session.commit()
        return make_response({"message": "Event deleted successfully"}), 200

    # Diseases Routes
    @app.route("/diseases", methods=["GET"])
    @jwt_required()
    def get_diseases():
        diseases = Disease.query.all()
        return jsonify([disease.to_dict() for disease in diseases]), 200

    @app.route("/diseases/<int:disease_id>", methods=["GET"])
    # @jwt_required()
    def get_disease(disease_id):
        disease = Disease.query.get(disease_id)
        if not disease:
            return jsonify({"error": "Disease not found"}), 404
        return jsonify(disease.to_dict()), 200

    @app.route("/diseases", methods=["POST"])
    @jwt_required()
    @auth_role("admin")

    def create_disease():
        data = request.json
        new_disease = Disease(
            name=data.get("name"),
            description=data.get("description"),
            symptoms=data.get("symptoms"),
            prevention_tips=data.get("prevention_tips"),
        )
        db.session.add(new_disease)
        db.session.commit()
        return make_response({"message": "Diseases added successfully"}), 201

    @app.route("/diseases/<int:disease_id>", methods=["DELETE"])
    @jwt_required()
    @auth_role("admin")
    def delete_disease(disease_id):
        disease = Disease.query.get(disease_id)
        if not disease:
            return jsonify({"error": "Disease not found"}), 404
        db.session.delete(disease)
        db.session.commit()
        return jsonify({"message": "Disease deleted successfully"}), 200

    @app.route("/get-affected-areas", methods=["GET"])
    def get_affected_areas():

        areas = AffectedArea.query.all()

        # Serialize using a to_dict method (ensure it's implemented in your model)
        return jsonify([area.to_dict() for area in areas]), 200

    @app.route("/affected-area", methods=["POST"])
    @jwt_required()
    @auth_role("admin")

    def save_affected_area():

        data = request.get_json()  # Ensure JSON payload
        if not data:
            return jsonify({"error": "Invalid or missing JSON payload"}), 400

        name = data.get("name", "Unnamed Area")
        location = data.get("location", "Unknown Location")
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        disease_count = data.get("disease_count", 0)

        if latitude is None or longitude is None:
            return jsonify({"error": "Latitude and Longitude are required"}), 400

        new_area = AffectedArea(
            name=name,
            location=location,
            latitude=latitude,
            longitude=longitude,
            disease_count=disease_count,
        )
        db.session.add(new_area)
        db.session.commit()

        return (
            jsonify(
                {"message": "Affected area saved successfully", "area_id": new_area.id}
            ),
            201,
        )

    @app.route("/save-location", methods=["POST"])
    def save_location():
        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON payload"}), 400

        latitude = data.get("latitude")
        longitude = data.get("longitude")

        if latitude is None or longitude is None:
            return jsonify({"error": "Latitude and Longitude are required"}), 400

        new_location = UserLocation(latitude=latitude, longitude=longitude)
        db.session.add(new_location)
        db.session.commit()

        return (
            jsonify(
                {
                    "message": "Location saved successfully",
                    "location_id": new_location.id,
                }
            ),
            201,
        )

    @app.route("/api/user-locations", methods=["GET"])
    def get_user_locations():
        locations = UserLocation.query.all()

        # Convert data into a list of dictionaries
        result = [
            {"latitude": loc.latitude, "longitude": loc.longitude} for loc in locations
        ]

        return jsonify(result), 200




    @app.route("/users/<int:user_id>/make_admin", methods=["PATCH"])
    @jwt_required()  # Ensure only authenticated users can perform this action
    @auth_role("admin")
    def make_admin(user_id):
        try:
            # Get the user by ID
            user = User.query.get(user_id)
            if not user:
                return jsonify({"error": "User not found"}), 404

        # Find or create the "admin" role
            admin_role = Role.query.filter_by(slug="admin").first()
            if not admin_role:
                admin_role = Role(name="Administrator", slug="admin")
                db.session.add(admin_role)
                db.session.commit()

        # Assign the "admin" role to the user
            if admin_role not in user.roles:
                user.roles.append(admin_role)
                db.session.commit()

            return jsonify({"message": f"User {user.username} is now an admin."}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"error": str(e)}), 500


    return app


# Only for running locally
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
