from sqlalchemy import Column, Integer, String, Text, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(300), nullable=False)
    subtitle = Column(String(300), nullable=False)
    body = Column(Text)
    posted_at = Column(Date)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE", onupdate="CASCADE"))
    category_id = Column(Integer, ForeignKey("categories.id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)

    user = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    comments = relationship("Comment", back_populates="post", cascade="all, delete")
    likes = relationship("Like", back_populates="post", cascade="all, delete")

    def to_dict(self, detailed=False):
        data = {
            "id": self.id,
            "title": self.title,
            "subtitle": self.subtitle,
            "posted_at": self.posted_at,
            "category_id": self.category_id,
            "author": {
                "id": self.user_id,
                "name":self.user.name
            },
            "category": self.category.name
        }

        if detailed:
            data["body"] = self.body
            data["author"]["email"] = self.user.email

        return data

