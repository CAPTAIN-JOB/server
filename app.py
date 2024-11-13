# app.py
from flask import Flask, jsonify, request,make_response
from flask_jwt_extended import JWTManager, create_refresh_token, create_access_token, jwt_required, get_jwt_identity, unset_jwt_cookies
from extensions import db, migrate
from Auth.auth import bp_auth
from models import *

import os

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
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
    
    
    
 
    # Events Routes
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
    
        new_event = Event(
            title=data.get('title'),
            description=data.get('description'),
            date=event_date,
            banner=data.get('banner'),
            created_by_user_id=data.get('created_by_user_id')
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



if __name__ == "__main__":
    app = create_app()
    app.run(port=5500, debug=True)
