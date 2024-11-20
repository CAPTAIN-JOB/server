# models.py
from extensions import db
import enum
from sqlalchemy import Enum
from sqlalchemy_serializer import SerializerMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
   
    
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    
class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)



class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'

    serialize_rules = ('-user',)  
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    banner = db.Column(db.String(255), nullable=True)
    created_by_user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship('User', backref=db.backref('events', lazy='subquery'))
    

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



 # tryied  this am getting  some  wied errors 
# class TransactionStatus(enum.Enum):
#     PENDING = "Pending"
#     COMPLETED = "Completed"
#     CANCELLED = "Cancelled"

class Transaction(db.Model):
    __tablename__ = 'transactions'

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(50), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pending")  
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)
    
    

 
