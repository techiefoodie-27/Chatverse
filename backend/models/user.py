from datetime import datetime
from extensions import db
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)

    username = db.Column(
        db.String(50),
        unique=True,
        nullable=False
    )

    email = db.Column(
        db.String(120),
        unique=True,
        nullable=False
    )
    password_hash = db.Column(
        db.String(255),
        nullable=False
    )
    is_verified = db.Column(
        db.Boolean,
        default=False
    )
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )
    def __repr__(self):
        return f"<User {self.username}>" 