from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import Optional
from random import randrange  # ✅ Import added

app = FastAPI()

# In-memory data store
my_posts = [
    {   
        "id" : 1,
        "title": "Hello Duniya",
        "content": "Learning FastAPI",
        "published": True,
        "ratings": "5 STAR"
    },
    {
        "id" : 2,
        "title": "Kya haal chaal",
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
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000)
    my_posts.append(post_dict)  # ✅ Fixed append

    return {"message": "Post created successfully", "post": post_dict}

#Endpoint for fetching the post with the specific ID
@app.get("/post/{post_id}")
def fetch_post(post_id : int = Path(..., description = "Id of the post to be fetched")):
    for existing_post in my_posts:
        if existing_post['id'] == post_id:
            return existing_post
    return {"Error" : "Post with the given ID doesn't exists"}

