from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.database.post_queries import (
    get_all_posts, get_post_by_id, insert_new_post,
    get_users_posts, delete_users_post, update_users_post
)
from app.database.category_queries import get_categories

post_bp = Blueprint("post_bp", __name__)

@post_bp.get("/")
@jwt_required()
def get_posts():
    # Query params
    limit = int(request.args.get("limit", 10))
    page = int(request.args.get("page", 1))
    sort_order = request.args.get("sort", "DESC")  # ASC or DESC
    category_id = request.args.get("category_id")

    offset = (page - 1) * limit

    posts = get_all_posts(limit=limit, offset=offset, sort_order=sort_order, category_id=category_id)
    return jsonify({
        "page": page,
        "limit": limit,
        "count": len(posts),
        "posts": posts
    }), 200

@post_bp.get("/<int:post_id>")
@jwt_required()
def get_post(post_id):
    post = get_post_by_id(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404
    return jsonify(post), 200

@post_bp.post("/")
@jwt_required()
def create_post():
    user_id = int(get_jwt_identity())
    data = request.get_json()
    if not all([data.get("title"), data.get("subtitle"), data.get("body"), data.get("category_id")]):
        return jsonify({"error": "Missing required fields"}), 400

    if data["category_id"] not in [category['id'] for category in get_categories()]:
        return jsonify({"error":"Category with this category id does not exist"}), 400

    success = insert_new_post(
        data["title"], data["subtitle"], data["body"],
        data["category_id"], user_id
    )
    if success:
        return jsonify({"message": "Post created"}), 201
    else:
        return jsonify({"error": "Failed to create post"}), 500

@post_bp.get("/my")
@jwt_required()
def my_posts():
    user_id = int(get_jwt_identity())
    return jsonify(get_users_posts(user_id)), 200

@post_bp.delete("/<int:post_id>")
@jwt_required()
def delete_post(post_id):
    user_id = int(get_jwt_identity())
    post = get_post_by_id(post_id)

    if not post:
        return jsonify({"error": "Post not found"}), 404
    
    if user_id != post["user_id"]:
        return jsonify({"error": "Unauthorized"}), 403  # Forbidden
    
    success = delete_users_post(post_id, user_id)
    if success:
        return jsonify({"message": "Deleted"}), 200
    else:
        return jsonify({"error": "Failed to delete"}), 500

@post_bp.put("/<int:post_id>")
@jwt_required()
def update_post(post_id):
    user_id = int(get_jwt_identity())
    post = get_post_by_id(post_id)

    if not post:
        return jsonify({"error": "Post not found"}), 404
    
    if user_id != post["user_id"]:
        return jsonify({"error": "Unauthorized"}), 403  # Forbidden
    
    data = request.get_json()
    if not all([data.get("title"), data.get("body"), data.get("subtitle"), data.get("category_id")]):
        return jsonify({"error": "Missing required fields"}), 400
    
    if data["category_id"] not in [c['id'] for c in get_categories()]:
        return jsonify({"error":"Category with this category id does not exist"}), 400
    
    success = update_users_post(post_id, data["title"], data["subtitle"],
                                data["body"], data["category_id"], user_id)
    if success:
        return jsonify({"message": "Updated"}), 200
    else:
        return jsonify({"error": "Failed to update"}), 500