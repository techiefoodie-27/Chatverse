from datetime import datetime, timedelta
from extensions import db
from utils.email import send_email


class OTPVerification(db.Model):

    __tablename__ = "otp_verifications"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    otp_code = db.Column(
        db.String(6),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    expires_at = db.Column(
        db.DateTime,
        default=lambda: datetime.utcnow() + timedelta(minutes=10)
    )

    is_used = db.Column(
        db.Boolean,
        default=False
    )