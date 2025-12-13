from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schemas.post import (
    PostCreateSchema,
    PostUpdateSchema,
)
from app.services.post_service import PostService
from app.repositories.category_repo import CategoryRepository
from pydantic import ValidationError

post_bp = Blueprint("post_bp", __name__)


@post_bp.get("/")
@jwt_required()
def get_posts():
    posts = PostService.get_all_posts()
    return jsonify(posts), 200


@post_bp.get("/<int:post_id>")
@jwt_required()
def get_post(post_id):
    post, error = PostService.get_post(post_id)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(post), 200


@post_bp.post("/")
@jwt_required()
def create_post():
    user_id = int(get_jwt_identity())
    try:
        data = PostCreateSchema.model_validate(request.get_json())
    except ValidationError as e:
        return jsonify({"errors":e.errors()})
    post, error = PostService.create_post(user_id, data)
    if error:
        return jsonify({"error":error}), 404
    return jsonify(post), 201


@post_bp.get("/my")
@jwt_required()
def my_posts():
    user_id = int(get_jwt_identity())
    posts = PostService.get_user_posts(user_id)
    return jsonify(posts), 200


@post_bp.get("/category/<int:category_id>")
@jwt_required
def get_posts_by_category(category_id):
    if not CategoryRepository.get_by_id(category_id):
        return jsonify({"error":"Category not found"}), 404 
    posts = PostService.get_by_category(category_id)
    return jsonify(posts), 200


@post_bp.delete("/<int:post_id>")
@jwt_required()
def delete_post(post_id):
    user_id = int(get_jwt_identity())

    success, error = PostService.delete_post(post_id, user_id)
    if not success:
        return jsonify({"error": error}), 400

    return jsonify({"message": "Deleted"}), 200


@post_bp.put("/<int:post_id>")
@jwt_required()
def update_post(post_id):
    user_id = int(get_jwt_identity())
    try:
        data = PostUpdateSchema.model_validate(request.get_json())
    except ValidationError as e:
        return jsonify({"error": e.errors()}), 400
    
    post, error = PostService.update_post(post_id, user_id, data)
    if error:
        return jsonify({"error": error}), 400

    return jsonify(post), 200
