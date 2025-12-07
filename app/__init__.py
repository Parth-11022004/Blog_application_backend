from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.core.config import Config
from app.core.database import engine, Base, SessionLocal

def create_app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = Config.SECRET_KEY

    # Initialize extensions
    CORS(app)
    JWTManager(app)

    # Create tables if they don't exist (optional, safe with existing tables)
    # Base.metadata.create_all(bind=engine)

    # Register blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.post_routes import post_bp
    from app.routes.comment_routes import comment_bp
    from app.routes.like_routes import like_bp

    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(post_bp, url_prefix="/api/posts")
    app.register_blueprint(comment_bp, url_prefix="/api/comments")
    app.register_blueprint(like_bp, url_prefix="/api/like")

    # Add a global teardown to remove DB session after each request
    @app.teardown_appcontext
    def remove_session(exception=None):
        SessionLocal.remove()

    # Optional: global error handler for JSON responses
    @app.errorhandler(404)
    def not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error"}), 500

    return app
