from pydantic import BaseModel, Field

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