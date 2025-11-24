from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database.like_queries import add_like, remove_like, get_like_count, check_user_liked

like_bp = Blueprint("like_bp", __name__)

@like_bp.post("/post/<int:post_id>")
@jwt_required()
def like_post(post_id):
    user_id = get_jwt_identity()
    success = add_like(user_id, post_id)
    if not success:
        return jsonify({"error": "Already liked or something went wrong"}), 400
    return jsonify({"message": "Post liked"}), 201


@like_bp.delete("/post/<int:post_id>")
@jwt_required()
def unlike_post(post_id):
    user_id = get_jwt_identity()
    success = remove_like(user_id, post_id)
    if not success:
        return jsonify({"error": "You haven’t liked this post"}), 404
    return jsonify({"message": "Like removed"}), 200


@like_bp.get("/post/<int:post_id>/count")
def get_post_likes(post_id):
    count = get_like_count(post_id)
    return jsonify({"likes": count}), 200


@like_bp.get("/post/<int:post_id>/status")
@jwt_required()
def check_liked(post_id):
    user_id = get_jwt_identity()
    liked = check_user_liked(user_id, post_id)
    return jsonify({"liked": liked}), 200
