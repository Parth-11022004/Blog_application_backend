from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class PostCreateSchema(BaseModel):
    title: str = Field(..., min_length=1)
    subtitle: str = Field(..., min_length=1)
    body: str
    category_id: int


class PostUpdateSchema(BaseModel):
    title: str
    subtitle: str
    body: str
    category_id: int


class PostOut(BaseModel):
    id: int
    title: str
    subtitle: str
    body: Optional[str]
    posted_at: Optional[date]
    user_id: int
    category_id: Optional[int]
    author: str
    category: Optional[str]

    class Config:
        from_attributes = True
