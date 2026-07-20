from flask_login import login_user, logout_user, login_required, current_user
from utils.security import check_password
from flask import Blueprint, request, jsonify
from extensions import db
from models.user import User
from utils.security import hash_password


auth = Blueprint("auth", __name__)


@auth.route("/register", methods=["POST"])
def register():

    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({
            "message": "All fields are required"
        }), 400


    existing_user = User.query.filter(
        (User.username == username) |
        (User.email == email)
    ).first()


    if existing_user:
        return jsonify({
            "message": "Username or email already exists"
        }), 409


    hashed_password = hash_password(password)


    new_user = User(
        username=username,
        email=email,
        password_hash=hashed_password
    )


    db.session.add(new_user)
    db.session.commit()


    return jsonify({
        "message": "User registered successfully"
    }), 201
@auth.route("/login", methods=["POST"])

def login():

    data = request.get_json()

    login_input = data.get("username_or_email")
    password = data.get("password")

    if not login_input or not password:
        return jsonify({
            "message": "Username/email and password required"
        }), 400


    user = User.query.filter(
        (User.username == login_input) |
        (User.email == login_input)
    ).first()

    
    if not user:
        return jsonify({
            "message": "User not found"
        }), 404

    if not user.is_verified:
        return jsonify({
            "message": "Please verify your email first"
        }), 403
        
    if not check_password(password, user.password_hash):
        return jsonify({
            "message": "Invalid password"
        }), 401


    login_user(user)

    return jsonify({
        "message": "Login successful",
        "username": user.username
    }), 200

@auth.route("/logout", methods=["POST"])
@login_required
def logout():

    logout_user()

    return jsonify({
        "message": "Logout successful"
    }), 200

@auth.route("/profile", methods=["GET"])
@login_required
def profile():

    return jsonify({
        "username": current_user.username,
        "email": current_user.email
    })