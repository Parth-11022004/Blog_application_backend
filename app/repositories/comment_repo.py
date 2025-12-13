from app.core.database import SessionLocal
from app.models.comment import Comment
from sqlalchemy.orm import joinedload


class CommentRepository:

    @staticmethod
    def get_by_id(comment_id: int):
        db = SessionLocal()
        comment = (
            db.query(Comment)
            .options(joinedload(Comment.user))
            .filter(Comment.id == comment_id)
            .first()
        )
        return comment

    @staticmethod
    def get_by_post(post_id: int):
        db = SessionLocal()
        comments = (
            db.query(Comment)
            .options(joinedload(Comment.user))
            .filter(Comment.post_id == post_id)
            .all()
        )
        return comments

    @staticmethod
    def get_by_user(user_id: int):
        db = SessionLocal()
        comments = (
            db.query(Comment)
            .options(joinedload(Comment.user))
            .filter(Comment.user_id == user_id)
            .all()
        )
        return comments

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
