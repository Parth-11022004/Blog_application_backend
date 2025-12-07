from app.core.database import SessionLocal
from app.models.like import Like


class LikeRepository:

    @staticmethod
    def add(user_id: int, post_id: int):
        db = SessionLocal()

        existing = db.query(Like).filter(
            Like.user_id == user_id,
            Like.post_id == post_id
        ).first()

        if existing:
            return None

        like = Like(user_id=user_id, post_id=post_id)
        db.add(like)
        db.commit()
        db.refresh(like)
        return like

    @staticmethod
    def remove(user_id: int, post_id: int):
        db = SessionLocal()

        like = db.query(Like).filter(
            Like.user_id == user_id,
            Like.post_id == post_id
        ).first()

        if not like:
            return False

        db.delete(like)
        db.commit()
        return True

    @staticmethod
    def user_liked(user_id: int, post_id: int):
        db = SessionLocal()
        return db.query(Like).filter(
            Like.user_id == user_id,
            Like.post_id == post_id
        ).first()

    @staticmethod
    def like_count(post_id: int):
        db = SessionLocal()
        return db.query(Like).filter(Like.post_id == post_id).count()
