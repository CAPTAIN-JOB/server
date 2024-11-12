# models.py
from extensions import db
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    

class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    banner = db.Column(db.String(255), nullable=True) 
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # Relationship 
    user = db.relationship('User', backref=db.backref('events', lazy=True))



class Disease(db.Model, SerializerMixin):
    __tablename__ = 'diseases'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True) 
    description = db.Column(db.Text, nullable=True) 
    symptoms = db.Column(db.Text, nullable=True) 
    prevention_tips = db.Column(db.Text, nullable=True)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) 


class Pay(db.Model, SerializerMixin):
    __tablename__ = 'payments'

    id = db.Column(db.Integer,primary_key=True)
    transaction_id = db.Column(db.String(100),unique=True,nullable=False)
    amount = db.Column(db.Float,nullable=False,)
    phone_number = db.Column(db.String(15),nullable=False)
    status = db.Column(db.String(20),nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
