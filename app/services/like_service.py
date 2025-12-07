from app.repositories.like_repo import LikeRepository
from app.repositories.post_repo import PostRepository


class LikeService:

    @staticmethod
    def add_like(user_id: int, post_id: int):
        if not PostRepository.get_by_id(post_id):
            return False, "Post not found"

        like = LikeRepository.add(user_id, post_id)
        if not like:
            return False, "Already liked"

        return True, None

    @staticmethod
    def remove_like(user_id: int, post_id: int):
        if not PostRepository.get_by_id(post_id):
            return False, "Post not found"

        removed = LikeRepository.remove(user_id, post_id)
        if not removed:
            return False, "You have not liked this post"

        return True, None
