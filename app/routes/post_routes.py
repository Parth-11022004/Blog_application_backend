from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schemas.post import (
    PostCreateSchema,
    PostUpdateSchema,
    PostOut
)
from app.services.post_service import PostService

post_bp = Blueprint("post_bp", __name__)


@post_bp.get("/")
@jwt_required()
def get_posts():
    posts = PostService.get_all_posts()
    return jsonify([PostOut.model_validate(p).model_dump() for p in posts]), 200


@post_bp.get("/<int:post_id>")
@jwt_required()
def get_post(post_id):
    post = PostService.get_post(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return PostOut.model_validate(post).model_dump(), 200


@post_bp.post("/")
@jwt_required()
def create_post():
    user_id = int(get_jwt_identity())
    data = PostCreateSchema.model_validate(request.get_json())
    try:
        post = PostService.create_post(user_id, data)
    except ValueError as e:
        return jsonify({"error":e}), 404
    else:
        return PostOut.model_validate(post).model_dump(), 201


@post_bp.get("/my")
@jwt_required()
def my_posts():
    user_id = int(get_jwt_identity())
    posts = PostService.get_user_posts(user_id)
    return jsonify([PostOut.model_validate(p).model_dump() for p in posts]), 200


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
    data = PostUpdateSchema.model_validate(request.get_json())

    post, error = PostService.update_post(post_id, user_id, data)
    if error:
        return jsonify({"error": error}), 400

    return PostOut.model_validate(post).model_dump(), 200
