from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    get_jwt_identity
)

from . import db
from .models import User

api = Blueprint("api", __name__)


@api.route("/health", methods=["GET"])
def health_check():
    return jsonify({"message": "HobbyBoard API is running"}), 200


@api.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data.get("username", "").strip()
    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not username or not email or not password:
        return jsonify({"error": "Username, email, and password are required"}), 400

    existing_username = User.query.filter_by(username=username).first()
    if existing_username:
        return jsonify({"error": "Username is already taken"}), 409

    existing_email = User.query.filter_by(email=email).first()
    if existing_email:
        return jsonify({"error": "Email is already registered"}), 409

    user = User(username=username, email=email)
    user.set_password(password)

    db.session.add(user)
    db.session.commit()

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "User created successfully",
        "user": user.to_dict(),
        "access_token": access_token
    }), 201


@api.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(identity=str(user.id))

    return jsonify({
        "message": "Login successful",
        "user": user.to_dict(),
        "access_token": access_token
    }), 200


@api.route("/me", methods=["GET"])
@jwt_required()
def get_current_user():
    user_id = int(get_jwt_identity())
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({"user": user.to_dict()}), 200


@api.route("/logout", methods=["POST"])
def logout():
    return jsonify({
        "message": "Logout successful. Remove the token on the frontend."
    }), 200