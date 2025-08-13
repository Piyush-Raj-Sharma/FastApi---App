from pydantic import BaseModel
from datetime import datetime

# Base schema (shared)
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# For creating a post
class PostCreate(PostBase):
    pass

# For updating a post
class PostUpdate(PostBase):
    pass

# Response schema
class PostResponse(PostBase):
    post_id: int
    created_at: datetime

    class Config:
        orm_mode = True  # Important for SQLAlchemy objects
