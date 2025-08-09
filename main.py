from fastapi import FastAPI, HTTPException, Path, status, Response
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

#Function to find the Index of the post with the given ID
def find_post_id(id):
    for index, post in enumerate(my_posts):
        if id == post["id"]:
            return index


@app.get("/")
def root():
    return {"message": "Hello from the social media app"}


@app.get("/posts")
def get_posts():
    return {"posts": my_posts}


@app.post("/posts", status_code = status.HTTP_201_CREATED)  #when we CREATE something we should give 201_created status code
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


# Endpoint for fetchiung the latest post
@app.get("/post/latest")
def fetch_latest_post():
    latetst_post = my_posts[len(my_posts) - 1]
    return {"latest post " : latetst_post}

# Endpoint: Fetch a specific post by its unique ID
@app.get("/post/{post_id}") 
def fetch_post(*, post_id: int = Path(..., description="ID of the post to retrieve"),
response : Response):
    """
    This endpoint searches for a post in 'my_posts' by matching the provided post_id.
    - If a matching post is found, it returns the post.
    - If no match is found, it returns an error message.
    """
    for existing_post in my_posts:
        if existing_post['id'] == post_id:
            return existing_post
        # response.status_code = status.HTTP_404_NOT_FOUND
        #Help to set the HTTP response code for better understanding to the frontend

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with the ID: {post_id} was not found")
    # return {"Error": "Post with the given ID does not exist"}

"""
IMPORTANT: Endpoint ordering in FastAPI
----------------------------------------
FastAPI processes routes in a **top-to-bottom** order. 
If we define '/post/{post_id}' before '/post/latest', 
then any request to '/post/latest' will match '/post/{post_id}' first, 
because FastAPI will interpret 'latest' as a post_id parameter.

Since 'latest' is not an integer, FastAPI will throw a validation error:
    "Input should be a valid integer, unable to parse string as an integer."

Solution: Always place more specific routes (e.g., '/post/latest') ABOVE 
dynamic parameter routes (e.g., '/post/{post_id}') to avoid conflicts.
"""

# Endpoint: Fetch the most recently added post
# @app.get("/post/latest")
# def fetch_latest_post():
#     """
#     Retrieves the last post from 'my_posts' list.
#     Assumes posts are stored in the order they were created.
#     """
#     latest_post = my_posts[len(my_posts) - 1]
#     return {"latest post": latest_post}


#Endpoint: Delete the post with the given ID
@app.delete("/post/{post_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(post_id : int ):
    index = find_post_id(post_id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the ID: {post_id} was not found")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
