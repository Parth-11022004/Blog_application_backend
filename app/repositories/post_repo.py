from app.core.database import SessionLocal
from app.models.post import Post
from sqlalchemy.orm import joinedload


class PostRepository:

    @staticmethod
    def get_all():
        db = SessionLocal()
        posts = (
            db.query(Post)
            .options(
                joinedload(Post.user),
                joinedload(Post.category)
            )
            .all()
        )
        return posts

    @staticmethod
    def get_by_id(post_id: int):
        db = SessionLocal()
        post = (
            db.query(Post)
            .options(
                joinedload(Post.user),
                joinedload(Post.category)
            )
            .filter(Post.id == post_id)
            .first()
        )
        return post

    @staticmethod
    def get_user_posts(user_id: int):
        db = SessionLocal()
        posts = (
            db.query(Post)
            .options(
                joinedload(Post.user),
                joinedload(Post.category)
            )
            .filter(Post.user_id == user_id)
            .all()
        )
        return posts

    @staticmethod
    def create(post: Post):
        db = SessionLocal()
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

    @staticmethod
    def get_by_category(category_id: int):
        db = SessionLocal()
        posts = (
            db.query(Post)
            .options(
                joinedload(Post.user),
                joinedload(Post.category)
            )
            .filter(Post.category_id == category_id)
            .all()
        )
        return posts

    @staticmethod
    def delete(post: Post):
        db = SessionLocal()
        db.delete(post)
        db.commit()

    @staticmethod
    def update(post: Post):
        db = SessionLocal()
        db.commit()
        db.refresh(post)
        return post
