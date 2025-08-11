from fastapi import FastAPI, HTTPException, Path, status, Response
from pydantic import BaseModel
from typing import Optional
from random import randrange  # ✅ Import added
import psycopg
# from psycopg.extras import RealDictCursor  #in psycopg2
# from psycopg.rows import dict_row  # Allows rows to be returned as dictionaries
from app.db import pool

import time

app = FastAPI()

# In-memory data store
my_posts = [
    {   
        "id": 1, 
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
This loop keeps trying to connect to a PostgreSQL database until it succeeds.
It is useful when the database might not be ready immediately (e.g., during app startup).

Steps:
1. Start an infinite loop (`while True`), so the connection attempt repeats until successful.
2. Inside `try`, attempt to connect to PostgreSQL using psycopg3:
   - `host`: Where the database is hosted (here, localhost).
   - `dbname`: Name of the database to connect to.
   - `user` & `password`: Database login credentials.
3. If the connection is successful, create a cursor (`conn.cursor`) with `row_factory=dict_row`:
   - This makes each row returned from queries behave like a Python dictionary 
     instead of a tuple, allowing access by column name.
4. Print a success message: "database connection established successfully".
5. Exit the loop using `break` (so we stop retrying once connected).
6. If an exception occurs (e.g., DB server is down, wrong credentials):
   - Print an error message.
   - Print the exact error details.
   - Wait 2 seconds (`time.sleep(2)`) before retrying the connection.
"""

# while True:
#     try:
#         with psycopg.connect(host='localhost', dbname='fastapi', user='postgres', password='@Piyush#123') as conn:
#             with conn.cursor(row_factory=dict_row) as cursor:
#                 print("database connection established successfully")
#         break
#     except Exception as error:
#         print("Connecting to database failed")
#         print("Error:", error)
#         time.sleep(2)

# -------Added this to db.py -----------

"""
    Using Pydantic's BaseModel to ensure incoming user data matches the schema:
    - Automatic type validation (int, str, bool, etc.)
    - Optional fields with default values
    - Optional fields with None if not provided
    - Returns detailed error messages on validation failure
"""

class Post(BaseModel):
    title: str                     # Required
    content: str                   # Required
    published: bool = True         # Optional with default
    # ratings: Optional[str] = None  # Completely optional

#Function to find the Index of the post with the given ID
def find_post_id(id):
    for index, post in enumerate(my_posts):
        if id == post["id"]:
            return index


@app.get("/")
def root():
    return {"message": "Hello from the social media app"}


@app.get("/posts")
async def get_posts():
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(""" Select * from posts""")
            posts = cursor.fetchall()
    return {"posts": posts}


@app.post("/posts", status_code = status.HTTP_201_CREATED)  #when we CREATE something we should give 201_created status code
def create_post(post: Post):  
    # Check if a post with the same title ID already exists
    for existing_post in my_posts:
        if existing_post["title"] == post.title:
            raise HTTPException(status_code=400, detail="This post ID already exists")
    
    # # Append new post as dictionary
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 100000)
    # my_posts.append(post_dict)  # ✅ Fixed append

    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """ , (post.title, post.content, post.published))  
            new_post = cursor.fetchone()
            conn.commit()
    return {"message": "Post created successfully", "post": new_post}


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
    # for existing_post in my_posts:
    #     if existing_post['id'] == post_id:
    #         return existing_post
        # response.status_code = status.HTTP_404_NOT_FOUND
        #Help to set the HTTP response code for better understanding to the frontend

    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(""" SELECT * FROM posts WHERE post_id = %s """, (post_id,))
            post = cursor.fetchone()
            if not post:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with the ID: {post_id} was not found")
            return post



    # raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with the ID: {post_id} was not found")
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
    # index = find_post_id(post_id)
    with pool.connection() as conn:
        with conn.cursor() as cursor :
            cursor.execute(""" DELETE FROM posts WHERE post_id = %s RETURNING * """, (post_id,))
            deleted_post = cursor.fetchone()
            conn.commit()
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the ID: {post_id} was not found")
    # my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


#Endpoint: Update post with the given ID
@app.put("/post/{post_id}")
def update_post(post_id : int, post : Post):

    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE post_id = %s RETURNING * """, (post.title, post.content, post.published, post_id))
            updated_post = cursor.fetchone()
            conn.commit()
    if updated_post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with the ID: {post_id} was not found")
    return {"data" : updated_post}
    # index = find_post_id(post_id)
    # if index == None:
    # post_dict = post.dict()
    # post_dict['id'] = post_id
    # my_posts[index] = post_dict


