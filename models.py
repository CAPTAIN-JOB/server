# models.py
import enum
from datetime import datetime

# from sqlalchemy import Enum
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy_serializer import SerializerMixin
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db


class User(db.Model, SerializerMixin):
    __tablename__ = "users"

    serialize_rules = ("-roles.users",)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50))
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    roles = db.relationship("Role", secondary="user_roles", back_populates="users")

    # Helper func
    # def has_role(self, role):
    #     return bool(
    #         role.query.join(Role.users)
    #         .filter(User.id == self.id)
    #         .filter(role.slug == role)
    #         .count()
    #         == 1
    #     )

    # def has_role(self, role_name):
    #     # Query the Role table to find a role matching the given name
    #     role = Role.query.filter_by(slug=role_name).first()
    #     if role and role in self.roles:
    #         return True
    #     return False

    def has_role(self, role_name):
        return (
            Role.query.filter(
                Role.users.any(id=self.id), Role.slug == role_name
            ).count()
            > 0
        )


class Role(db.Model, SerializerMixin):
    __tablename__ = "roles"

    serialize_rules = ("-users.roles",)

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    slug = db.Column(db.String(50), nullable=False, unique=True)

    users = db.relationship("User", secondary="user_roles", back_populates="roles")


# association table
class UserRole(db.Model):
    __tablename__ = "user_roles"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"), primary_key=True)


class TokenBlocklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(36), nullable=False, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)


class Event(db.Model, SerializerMixin):
    __tablename__ = "events"

    serialize_rules = ("-user",)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    banner = db.Column(db.String(255), nullable=True)
    created_by_user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    user = db.relationship("User", backref=db.backref("events", lazy="subquery"))


class Disease(db.Model, SerializerMixin):
    __tablename__ = "diseases"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=True)
    symptoms = db.Column(db.Text, nullable=True)
    prevention_tips = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Pay(db.Model, SerializerMixin):
    __tablename__ = "payments"

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False)
    amount = db.Column(
        db.Float,
        nullable=False,
    )
    phone_number = db.Column(db.String(15), nullable=False)
    status = db.Column(db.String(20), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


# tryied  this am getting  some  wied errors
# class TransactionStatus(enum.Enum):
#     PENDING = "Pending"
#     COMPLETED = "Completed"
#     CANCELLED = "Cancelled"


class Transaction(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.String(50), unique=True, nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Pending")
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class AffectedArea(db.Model, SerializerMixin):
    __tablename__ = "affected_areas"

    serialize_rules = ("-maps",)

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    location = db.Column(db.String, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    disease_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    maps = db.relationship(
        "Map", backref="affected_area", lazy=True, cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.Index("idx_affected_area_lat_lon", "latitude", "longitude"),
        db.Index("idx_disease_count", "disease_count"),
    )


# @validates("latitude", "longitude")
# def validate_coordinates(self, key, value):
#     if key == "latitude" and (value < -90 or value > 90):
#         raise ValueError("Latitude must be between -90 and 90")
#     if key == "longitude" and (value < -180 or value > 180):
#         raise ValueError("Longitude must be between -180 and 180")
#     return value


class Map(db.Model):
    __tablename__ = "maps"

    id = db.Column(db.Integer, primary_key=True)
    affected_area_id = db.Column(
        db.Integer, db.ForeignKey("affected_areas.id"), nullable=False
    )
    map_data = db.Column(JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())


class UserLocation(db.Model):
    __tablename__ = "user_locations"

    id = db.Column(db.Integer, primary_key=True)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(
        db.DateTime,
        default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp(),
    )

    __table_args__ = (db.Index("idx_lat_lon", "latitude", "longitude"),)
