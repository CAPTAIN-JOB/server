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


class Pay(db.Model, SerializerMixin):
    __tablename__ = 'payments'

    id = db.Column(db.Integer,primary_key=True)
    transaction_id = db.Column(db.String(100),unique=True,nullable=False)
    amount = db.Column(db.Float,nullable=False,)
    phone_number = db.Column(db.String(15),nullable=False)
    status = db.Column(db.String(20),nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
