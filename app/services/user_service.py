from werkzeug.security import generate_password_hash, check_password_hash
from app.repositories.user_repo import UserRepository
from app.models.user import User


class UserService:

    @staticmethod
    def register_user(data):
        if UserRepository.get_by_email(data.email) or UserRepository.get_by_username(data.username):
            return None, "Email or username already exists"
        
        hashed_pw = generate_password_hash(data.password)

        new_user = User(
            name=data.name,
            username=data.username,
            email=data.email,
            password=hashed_pw
        )

        user = UserRepository.create(new_user)
        return user.to_dict(), None

    @staticmethod
    def authenticate_user(email: str, password: str):
        user = UserRepository.get_by_email(email)
        if not user:
            return None
        if not check_password_hash(user.password, password):
            return None
        return user.to_dict()
    
    def delete_user(user_id: int):
        user = UserRepository.get_by_id(user_id)
        if not user:
            return False, "User not found"
        UserRepository.delete(user_id)
        return True, None