from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from pydantic import ValidationError
from app.schemas.comment import (
    CommentCreateSchema,
    CommentUpdateSchema
)
from app.services.comment_service import CommentService

comment_bp = Blueprint("comment_bp", __name__)


@comment_bp.get("/<int:comment_id>")
@jwt_required()
def get_comment(comment_id):
    comment, error = CommentService.get_comment_by_id(comment_id)
    if error:
        return jsonify({"error":error}), 404
    return jsonify(comment), 200

@comment_bp.get("/post/<int:post_id>")
@jwt_required()
def get_comments_by_post(post_id):
    comments, error = CommentService.get_comments_by_post(post_id)
    if error:
        return jsonify({"error": error}), 404
    return jsonify(comments), 200

@comment_bp.get("/my")
@jwt_required()
def my_comments():
    user_id = int(get_jwt_identity())
    comments = CommentService.get_current_users_comments(user_id)
    return jsonify(comments), 200

@comment_bp.post("/post/<int:post_id>")
@jwt_required()
def create_comment(post_id):
    user_id = int(get_jwt_identity())
    try:
        data = CommentCreateSchema.model_validate(request.get_json())
    except ValidationError as e:
        return jsonify({"error":e.errors()})
    
    comment, error = CommentService.create_comment(user_id, post_id, data)
    if error:
        return jsonify({"error": error}), 400

    return jsonify(comment), 201


@comment_bp.put("/<int:comment_id>")
@jwt_required()
def edit_comment(comment_id):
    user_id = int(get_jwt_identity())
    try:
        data = CommentUpdateSchema.model_validate(request.get_json())
    except ValidationError as e:
        return jsonify({"error":e.errors()})
    comment, error = CommentService.update_comment(comment_id, user_id, data)
    if error:
        return jsonify({"error": error}), 400

    return jsonify(comment), 200


@comment_bp.delete("/<int:comment_id>")
@jwt_required()
def remove_comment(comment_id):
    user_id = int(get_jwt_identity())

    success, error = CommentService.delete_comment(comment_id, user_id)

    if error:
        return jsonify({"error": error}), 400

    return jsonify({"message": "Comment deleted successfully"}), 200
