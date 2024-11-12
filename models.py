# models.py
from extensions import db
from sqlalchemy_serializer import SerializerMixin

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
