# app.py
from flask import Flask
from extensions import db, migrate
from Auth.auth import bp_auth

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///data.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(bp_auth, url_prefix='/auth')

    return app

# Only for running locally
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
