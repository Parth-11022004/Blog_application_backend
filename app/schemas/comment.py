from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class CommentCreateSchema(BaseModel):
    body: str = Field(..., min_length=1)


class CommentUpdateSchema(BaseModel):
    body: str = Field(..., min_length=1)


class CommentOut(BaseModel):
    id: int
    body: str
    posted_at: Optional[date]
    user_id: int
    post_id: int

    class Config:
        from_attributes = True
