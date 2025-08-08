from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# In-memory data store
my_posts = [
    {
        "title": 1,
        "content": "Learning FastAPI",
        "published": True,
        "ratings": "5 STAR"
    },
    {
        "title": 2,
        "content": "Learned React/Redux",
        "published": False,
        "ratings": "4 STAR"
    }
]

"""
    Using Pydantic's BaseModel to ensure incoming user data matches the schema:
    - Automatic type validation (int, str, bool, etc.)
    - Optional fields with default values
    - Optional fields with None if not provided
    - Returns detailed error messages on validation failure
"""

class Post(BaseModel):
    title: int                     # Required
    content: str                   # Required
    published: bool = True         # Optional with default
    ratings: Optional[str] = None  # Completely optional


@app.get("/")
def root():
    return {"message": "Hello from the social media app"}


@app.get("/posts")
def get_posts():
    return {"posts": my_posts}


@app.post("/posts")
def create_post(post: Post):
    # Check if a post with the same title ID already exists
    for existing_post in my_posts:
        if existing_post["title"] == post.title:
            raise HTTPException(status_code=400, detail="This post ID already exists")
    
    # Append new post as dictionary
    my_posts.append(post.dict())
    return {"message": "Post created successfully", "post": post}
