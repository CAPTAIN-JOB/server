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

    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "username": self.username,
            "email": self.email,
            "created_at": self.created_at.isoformat()
        }

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

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "date": self.date.isoformat(),
            "banner": self.banner,
            "created_by_user_id": self.created_by_user_id,
            "created_at": self.created_at.isoformat()
        }

    def __repr__(self):
        return f"<Event(id={self.id}, title='{self.title}', date={self.date}, created_by_user_id={self.created_by_user_id})>"




class Disease(db.Model, SerializerMixin):
    __tablename__ = 'diseases'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True) 
    description = db.Column(db.Text, nullable=True) 
    symptoms = db.Column(db.Text, nullable=True) 
    prevention_tips = db.Column(db.Text, nullable=True)  
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False) 


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "symptoms": self.symptoms,
            "prevention_tips": self.prevention_tips,
            "created_at": self.created_at.isoformat()
        }


    def __repr__(self):
        return f"<Disease(id={self.id}, name='{self.name}')>"
