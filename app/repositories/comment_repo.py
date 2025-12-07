from app.core.database import SessionLocal
from app.models.comment import Comment


class CommentRepository:

    @staticmethod
    def get_all():
        db = SessionLocal()
        return db.query(Comment).all()

    @staticmethod
    def get_by_id(comment_id: int):
        db = SessionLocal()
        return db.query(Comment).filter(Comment.id == comment_id).first()

    @staticmethod
    def get_by_post(post_id: int):
        db = SessionLocal()
        return db.query(Comment).filter(Comment.post_id == post_id).all()

    @staticmethod
    def get_by_user(user_id: int):
        db = SessionLocal()
        return db.query(Comment).filter(Comment.user_id == user_id).all()

    @staticmethod
    def create(comment: Comment):
        db = SessionLocal()
        db.add(comment)
        db.commit()
        db.refresh(comment)
        return comment

    @staticmethod
    def update(comment: Comment):
        db = SessionLocal()
        db.commit()
        db.refresh(comment)
        return comment

    @staticmethod
    def delete(comment: Comment):
        db = SessionLocal()
        db.delete(comment)
        db.commit()
