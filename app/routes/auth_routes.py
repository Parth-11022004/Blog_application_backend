from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token

from app.schemas.user import UserLoginSchema, UserRegisterSchema, UserOut
from app.services.user_service import UserService

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.post("/signup")
def signup():

    data = UserRegisterSchema.model_validate(request.get_json())
    try:
        user = UserService.register_user(data)
    except ValueError as e:
        return jsonify({"error":e}), 409
    else:
        return jsonify({"message": "User registered successfully", "user": UserOut.model_validate(user).model_dump()}), 201


@auth_bp.post("/login")
def login():
    data = UserLoginSchema.model_validate(request.get_json())

    user = UserService.authenticate_user(data.email, data.password)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401

    token = create_access_token(identity=str(user.id))

    return jsonify({"access_token": token}), 200

