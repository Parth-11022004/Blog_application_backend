from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = Config.SECRET_KEY

    CORS(app)
    JWTManager(app)

    #register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.post_routes import post_bp
    from app.routes.comment_routes import comment_bp
    from app.routes.like_routes import like_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(post_bp, url_prefix="/api/posts")
    app.register_blueprint(comment_bp, url_prefix="/api/comments")
    app.register_blueprint(like_bp, url_prefix="/api/like")

    return app
