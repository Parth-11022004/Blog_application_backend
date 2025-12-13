from datetime import date
from app.models.comment import Comment
from app.repositories.comment_repo import CommentRepository
from app.repositories.post_repo import PostRepository

class CommentService:

    @staticmethod
    def get_comment_by_id(comment_id: int):
        comment = CommentRepository.get_by_id(comment_id)
        if not comment:
            return None, "Comment not found"
        return comment.to_dict(detailed=True), None
    
    @staticmethod
    def get_comments_by_post(post_id: int):
        if not PostRepository.get_by_id(post_id):
            return None, "Post not found"
        comments = CommentRepository.get_by_post(post_id)
        return [c.to_dict(detailed=False) for c in comments], None

    @staticmethod
    def get_current_users_comments(user_id: int):
        comments = CommentRepository.get_by_user(user_id)
        return [c.to_dict(detailed=False) for c in comments]

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

        comment = CommentRepository.create(comment)
        return comment.to_dict(detailed=True), None

    @staticmethod
    def update_comment(comment_id: int, user_id: int, data):
        comment = CommentRepository.get_by_id(comment_id)
        if not comment:
            return None, "Comment not found"

        if comment.user_id != user_id:
            return None, "Unauthorized"

        comment.body = data.body

        comment = CommentRepository.update(comment)
        return comment.to_dict(detailed=True), None

    @staticmethod
    def delete_comment(comment_id: int, user_id: int):
        comment = CommentRepository.get_by_id(comment_id)
        if not comment:
            return False, "Comment not found"

        if comment.user_id != user_id:
            return False, "Unauthorized"

        CommentRepository.delete(comment)
        return True, None
