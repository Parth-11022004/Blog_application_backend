from datetime import date

from app.models.post import Post
from app.repositories.post_repo import PostRepository
from app.repositories.category_repo import CategoryRepository


class PostService:

    @staticmethod
    def get_all_posts():
        posts = PostRepository.get_all()
        return [p.to_dict(detailed=False) for p in posts]

    @staticmethod
    def get_post(post_id: int):
        post = PostRepository.get_by_id(post_id)
        return post.to_dict(detailed=True) if post else None

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

        post = PostRepository.create(post)
        return post.to_dict(detailed=True)

    @staticmethod
    def get_user_posts(user_id: int):
        posts = PostRepository.get_user_posts(user_id)
        return [p.to_dict(detailed=False) for p in posts]
    
    def get_by_category(category_id: int):
        posts = PostRepository.get_by_category(category_id)
        if not posts:
            return None
        return [p.to_dict(detailed=False) for p in posts]

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

        post = PostRepository.update(post)
        return post.to_dict(detailed=True), None
