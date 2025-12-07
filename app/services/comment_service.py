from datetime import date

from app.models.comment import Comment
from app.repositories.comment_repo import CommentRepository
from app.repositories.post_repo import PostRepository


class CommentService:

    @staticmethod
    def get_all_comments():
        return CommentRepository.get_all()

    @staticmethod
    def get_comments_by_post(post_id: int):
        if not CommentRepository.get_by_post(post_id):
            return None, "Post not found"
        comments = CommentRepository.get_by_post(post_id)
        return comments, None

    @staticmethod
    def get_current_users_comments(user_id: int):
        return CommentRepository.get_by_user(user_id)

    @staticmethod
    def get_comment_by_id(comment_id: int):
        if not CommentRepository.get_by_id(comment_id):
            return None, "Comment not found"
        comment = CommentRepository.get_by_id(comment_id)
        return comment, None

    @staticmethod
    def create_comment(user_id: int, post_id: int, data):
        post = PostRepository.get_by_id(post_id)
        if not post:
            return None, "Post not found"

        comment = Comment(
            body=data.body,
            user_id=user_id,
            post_id=post_id,
            posted_at=date.today()
        )

        return CommentRepository.create(comment), None

    @staticmethod
    def update_comment(comment_id: int, user_id: int, data):
        comment = CommentRepository.get_by_id(comment_id)
        if not comment:
            return None, "Comment not found"

        if comment.user_id != user_id:
            return None, "Unauthorized"

        comment.body = data.body

        return CommentRepository.update(comment), None

    @staticmethod
    def delete_comment(comment_id: int, user_id: int):
        comment = CommentRepository.get_by_id(comment_id)
        if not comment:
            return False, "Comment not found"

        if comment.user_id != user_id:
            return False, "Unauthorized"

        CommentRepository.delete(comment)
        return True, None
