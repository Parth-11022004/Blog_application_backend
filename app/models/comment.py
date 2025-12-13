from sqlalchemy import Column, Integer, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    body = Column(Text, nullable=False)
    posted_at = Column(Date)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="comments")
    post = relationship("Post", back_populates="comments")

    def to_dict(self, detailed=False):
        data = {
            "id":self.id,
            "body":self.body,
            "posted_at": self.posted_at,
            "post_id":self.post_id,
            "user": {
                "id":self.user_id,
                "name":self.user.name
            }
        }
        if detailed:
            data["user"]["email"] = self.user.email

        return data