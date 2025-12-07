from app.core.database import SessionLocal
from app.models.user import User


class UserRepository:

    @staticmethod
    def create(user: User):
        db = SessionLocal()
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    @staticmethod
    def get_by_email(email: str):
        db = SessionLocal()
        return db.query(User).filter(User.email == email).first()

    @staticmethod
    def get_by_username(username: str):
        db = SessionLocal()
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def get_by_id(user_id: int):
        db = SessionLocal()
        return db.query(User).filter(User.id == user_id).first()
