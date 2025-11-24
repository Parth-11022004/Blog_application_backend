from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from app.database.user_queries import insert_registration_data, get_user_by_email

auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.post("/signup")
def signup():
    data = request.get_json()
    name, username, email, password = (
        data.get("name"),
        data.get("username"),
        data.get("email"),
        data.get("password")
    )

    if not all([name, username, email, password]):
        return jsonify({"error": "Missing required fields"}), 400

    password_hash = generate_password_hash(password)
    if not insert_registration_data(name, username, email, password_hash):
        return jsonify({"error": "Email or username exists"}), 409

    return jsonify({"message": "User registered successfully"}), 201


@auth_bp.post("/login")
def login():
    data = request.get_json()
    email, password = data.get("email"), data.get("password")

    user = get_user_by_email(email)
    if not user or not check_password_hash(user["password"], password):
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user["id"]))
    return jsonify({"access_token": token}), 200
