from pydantic import BaseModel, Field

class CommentCreateSchema(BaseModel):
    body: str = Field(..., min_length=1)

class CommentUpdateSchema(BaseModel):
    body: str = Field(..., min_length=1)