from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database.comment_queries import (
    insert_comment,
    get_all_comments,
    get_comments_by_post,
    get_comments_by_user,
    get_comment_by_id,
    update_comment,
    delete_comment
)
from app.database.post_queries import get_all_posts_ids
comment_bp = Blueprint("comments", __name__)

@comment_bp.route("/", methods=["GET"])
@jwt_required()
def all_comments():
    post_id = request.args.get("post_id")
    user_id = request.args.get("user_id")

    if post_id:
        comments = get_comments_by_post(post_id)
    elif user_id:
        comments = get_comments_by_user(user_id)
    else:
        comments = get_all_comments()

    return jsonify(comments), 200

@comment_bp.route("/post/<int:post_id>", methods=["GET"])
@jwt_required()
def comments_for_post(post_id):
    if post_id not in get_all_posts_ids():
        return jsonify({"error":"post not found"}), 404
    
    comments = get_comments_by_post(post_id)
    return jsonify(comments), 200

@comment_bp.route("/user", methods=["GET"])
@jwt_required()
def user_comments():
    user_id = int(get_jwt_identity())
    comments = get_comments_by_user(user_id)
    return jsonify(comments), 200

@comment_bp.route("/post/<int:post_id>", methods=["POST"])
@jwt_required()
def create_comment(post_id):
    if post_id not in get_all_posts_ids():
        return jsonify({"error":"post doesnt exist"}), 404
    
    user_id = int(get_jwt_identity())
    data = request.get_json()

    if (not data) or ("body" not in data) or (not data.get("body")):
        return jsonify({"error": "Comment body required"}), 400

    success = insert_comment(data["body"], user_id, post_id)
    if success:
        return jsonify({"message": "comment created"}), 201
    else:
        return jsonify({"error": "Failed to add comment"}), 500

@comment_bp.route("/<int:comment_id>", methods=["PUT"])
@jwt_required()
def edit_comment(comment_id):
    user_id = int(get_jwt_identity())
    existing_comment = get_comment_by_id(comment_id)

    if not existing_comment:
        return jsonify({"error": "Comment not found"}), 404

    if existing_comment["user_id"] != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    if (not data) or ("body" not in data) or (not data.get("body")):
        return jsonify({"error": "New comment body required"}), 400

    updated = update_comment(comment_id, data["body"])
    if updated:
        return jsonify({"message": "Comment updated successfully"}), 200
    return jsonify({"error": "Failed to update comment"}), 500

@comment_bp.route("/<int:comment_id>", methods=["DELETE"])
@jwt_required()
def remove_comment(comment_id):
    user_id = int(get_jwt_identity())
    existing_comment = get_comment_by_id(comment_id)

    if not existing_comment:
        return jsonify({"error": "Comment not found"}), 404

    if existing_comment["user_id"] != user_id:
        return jsonify({"error": "Unauthorized"}), 403

    deleted = delete_comment(comment_id)
    if deleted:
        return jsonify({"message": "Comment deleted successfully"}), 200
    return jsonify({"error": "Failed to delete comment"}), 500
