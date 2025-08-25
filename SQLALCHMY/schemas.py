from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Base schema (shared)
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True

# For creating a post
class PostCreate(PostBase):
    pass

# For updating a post
class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None

# Response schema
class PostResponse(PostBase):
    post_id: int
    created_at: datetime

    class Config:
        orm_mode = True  # Important for SQLAlchemy objects


# --------------------------------------------------------
# USER SCHEMAS

class UserBase(BaseModel):
    email: EmailStr
    password: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    password: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(BaseModel):
    user_id: int
    email: EmailStr
    password: str
    created_at: datetime

    class Config:
        orm_mode = True
        
# -----------------------------------------

class UserLogin(BaseModel):
    email: EmailStr
    password: str