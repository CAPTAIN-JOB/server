# app.py
from flask import Flask, jsonify, request
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

    # Register blueprints
    app.register_blueprint(bp_auth, url_prefix='/auth')
     # app.register_blueprint(bp_auth)


    # Users Routes
    # @app.route('/users', methods=['GET'])
    # def get_users():
    #     users = User.query.all()
    #     return jsonify([user.to_dict() for user in users]), 200


    # @app.route('/users/<int:user_id>', methods=['GET'])
    # def get_user(user_id):
    #     user = User.query.get(user_id)
    #     if not user:
    #         return jsonify({"error": "User not found"}), 404
    #     return jsonify(user.to_dict()), 200


    # @app.route('/users', methods=['POST'])
    # def create_user():
    #     data = request.json
    #     new_user = User(
    #        name=data.get('name'),
    #        username=data.get('username'),
    #        email=data.get('email'),
    #        password=data.get('password')
    #     )
    #     db.session.add(new_user)
    #     db.session.commit()
    #     return jsonify(new_user.to_dict()), 201


    # @app.route('/users/<int:user_id>', methods=['DELETE'])
    # def delete_user(user_id):
    #     user = User.query.get(user_id)
    #     if not user:
    #         return jsonify({"error": "User not found"}), 404
    #     db.session.delete(user)
    #     db.session.commit()
    #     return jsonify({"message": "User deleted successfully"}), 200

    @app.route('/events', methods=['GET'])
    def get_events():
        events = Event.query.all()
        return jsonify([event.serialize() for event in events]), 200


    @app.route('/events/<int:event_id>', methods=['GET'])
    def get_event(event_id):
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Event not found"}), 404
        return jsonify(event.serialize()), 200


    @app.route('/events', methods=['POST'])
    def create_event():
        data = request.json
        new_event = Event(
        title=data.get('title'),
        description=data.get('description'),
        date=data.get('date'),
        banner=data.get('banner'),
        created_by_user_id=data.get('created_by_user_id')
    )
        db.session.add(new_event)
        db.session.commit()
        return jsonify(new_event.serialize()), 201


    @app.route('/events/<int:event_id>', methods=['DELETE'])
    def delete_event(event_id):
        event = Event.query.get(event_id)
        if not event:
            return jsonify({"error": "Event not found"}), 404
        db.session.delete(event)
        db.session.commit()
        return jsonify({"message": "Event deleted successfully"}), 200


# Diseases Routes
    @app.route('/diseases', methods=['GET'])
    def get_diseases():
        diseases = Disease.query.all()
        
        return jsonify([disease.serialize() for disease in diseases]), 200


    @app.route('/diseases/<int:disease_id>', methods=['GET'])
    def get_disease(disease_id):
        disease = Disease.query.get(disease_id)
        if not disease:
            return jsonify({"error": "Disease not found"}), 404
        return jsonify(disease.serialize()), 200


    @app.route('/diseases', methods=['POST'])
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
        return jsonify(new_disease.serialize()), 201


    @app.route('/diseases/<int:disease_id>', methods=['DELETE'])
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
    app.run(host='0.0.0.0', port=5500, debug=True)
