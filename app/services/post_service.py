from datetime import date

from app.models.post import Post
from app.repositories.post_repo import PostRepository
from app.repositories.category_repo import CategoryRepository


class PostService:

    @staticmethod
    def get_all_posts():
        return PostRepository.get_all()

    @staticmethod
    def get_post(post_id: int):
        return PostRepository.get_by_id(post_id)

    @staticmethod
    def create_post(user_id: int, data):
        if not CategoryRepository.get_by_id(data.category_id):
            raise ValueError("Category does not exist")

        post = Post(
            title=data.title,
            subtitle=data.subtitle,
            body=data.body,
            posted_at=date.today(),
            category_id=data.category_id,
            user_id=user_id
        )

        return PostRepository.create(post)

    @staticmethod
    def get_user_posts(user_id: int):
        return PostRepository.get_user_posts(user_id)

    @staticmethod
    def delete_post(post_id: int, user_id: int):
        post = PostRepository.get_by_id(post_id)
        if not post:
            return False, "Post not found"

        if post.user_id != user_id:
            return False, "Unauthorized"

        PostRepository.delete(post)
        return True, None

    @staticmethod
    def update_post(post_id: int, user_id: int, data):
        post = PostRepository.get_by_id(post_id)
        if not post:
            return None, "Post not found"

        if post.user_id != user_id:
            return None, "Unauthorized"

        if not CategoryRepository.get_by_id(data.category_id):
            return None, "Category does not exist"

        post.title = data.title
        post.subtitle = data.subtitle
        post.body = data.body
        post.category_id = data.category_id

        updated = PostRepository.update(post)
        return updated, None
