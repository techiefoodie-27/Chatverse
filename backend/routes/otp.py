from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from utils.email import send_email
from models.otp import OTPVerification
import random


otp = Blueprint("otp", __name__)


@otp.route("/send-otp", methods=["POST"])
def send_otp():

    data = request.json

    email = data.get("email")

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404


    generated_otp = str(random.randint(100000, 999999))


    new_otp = OTPVerification(
        user_id=user.id,
        otp_code=generated_otp
    )


    db.session.add(new_otp)
    db.session.commit()


    send_email(email, generated_otp)

    return jsonify({
        "message": "OTP sent to your email"
    }), 200
from datetime import datetime


@otp.route("/verify-otp", methods=["POST"])
def verify_otp():

    data = request.json

    email = data.get("email")
    entered_otp = data.get("otp")


    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({
            "message": "User not found"
        }), 404


    otp_record = OTPVerification.query.filter_by(
        user_id=user.id,
        otp_code=entered_otp,
        is_used=False
    ).order_by(
        OTPVerification.created_at.desc()
    ).first()


    if not otp_record:
        return jsonify({
            "message": "Invalid OTP"
        }), 400


    if otp_record.expires_at < datetime.utcnow():
        return jsonify({
            "message": "OTP expired"
        }), 400


    user.is_verified = True
    otp_record.is_used = True

    db.session.commit()


    return jsonify({
        "message": "Email verified successfully"
    }), 200