from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.schemas.user import UserLoginSchema, UserRegisterSchema
from app.services.user_service import UserService
from pydantic import ValidationError

user_bp = Blueprint("user_bp", __name__)

@user_bp.post("/signup")
def signup():
    try:
        data = UserRegisterSchema.model_validate(request.get_json())
    except ValidationError as e:
        return jsonify({"error":e.errors()})
    user, error = UserService.register_user(data)
    if error:
        return jsonify({"error":error}), 409
    else:
        return jsonify({"message": "User registered successfully", "user": user}), 201


@user_bp.post("/login")
def login():
    try:
        data = UserLoginSchema.model_validate(request.get_json())
    except ValidationError as e:
        return jsonify({"error":e.errors()})
    user = UserService.authenticate_user(data.email, data.password)
    if not user:
        return jsonify({"error": "Invalid credentials"}), 401
    token = create_access_token(identity=str(user.id))
    return jsonify({"access_token": token}), 200

@user_bp.delete("/")
@jwt_required
def delete_user(user_id):
    user_id = int(get_jwt_identity())
    success, error = UserService.delete_user(user_id)
    if error:
        return jsonify({"error":error}), 404
    return jsonify({"message":"user deleted successfully"}), 200