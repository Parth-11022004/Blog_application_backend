from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.like_service import LikeService

like_bp = Blueprint("like_bp", __name__)


@like_bp.post("/post/<int:post_id>")
@jwt_required()
def like_post(post_id):
    user_id = int(get_jwt_identity())

    success, error = LikeService.add_like(user_id, post_id)
    if not success:
        return jsonify({"error": error}), 400

    return jsonify({"message": "Post liked"}), 201


@like_bp.delete("/post/<int:post_id>")
@jwt_required()
def unlike_post(post_id):
    user_id = int(get_jwt_identity())

    success, error = LikeService.remove_like(user_id, post_id)
    if not success:
        return jsonify({"error": error}), 404

    return jsonify({"message": "Like removed"}), 200
