from app.core.database import SessionLocal
from app.models.post import Post


class PostRepository:

    @staticmethod
    def get_all():
        db = SessionLocal()
        return db.query(Post).all()

    @staticmethod
    def get_by_id(post_id: int):
        db = SessionLocal()
        return db.query(Post).filter(Post.id == post_id).first()

    @staticmethod
    def get_user_posts(user_id: int):
        db = SessionLocal()
        return db.query(Post).filter(Post.user_id == user_id).all()

    @staticmethod
    def create(post: Post):
        db = SessionLocal()
        db.add(post)
        db.commit()
        db.refresh(post)
        return post

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
