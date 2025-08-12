from fastapi import FastAPI, HTTPException, Path, status, Response, Depends
from pydantic import BaseModel
from random import randrange 
from app.db import pool
from .database import Base, engine
from . import models
from .database import SessionLocal
from sqlalchemy.orm import Session
from .models import Post

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

@app.post("/users")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    new_user = Post(name=name, email=email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# @app.get("/")
# def root():
#     return {"message": "Hello from the social media app"}


# @app.get("/posts")
# async def get_posts():
#     with pool.connection() as conn:
#         with conn.cursor() as cursor:
#             cursor.execute(""" Select * from posts""")
#             posts = cursor.fetchall()
#     return {"posts": posts}


# @app.post("/posts", status_code = status.HTTP_201_CREATED)  #when we CREATE something we should give 201_created status code
# def create_post(post: Post):  
#     # Check if a post with the same title ID already exists
#     for existing_post in my_posts:
#         if existing_post["title"] == post.title:
#             raise HTTPException(status_code=400, detail="This post ID already exists")

#     with pool.connection() as conn:
#         with conn.cursor() as cursor:
#             cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """ , (post.title, post.content, post.published))  
#             new_post = cursor.fetchone()
#             conn.commit()
#     return {"message": "Post created successfully", "post": new_post}


# # Endpoint for fetchiung the latest post
# # @app.get("/post/latest")
# # def fetch_latest_post():
# #     latetst_post = my_posts[len(my_posts) - 1]
# #     return {"latest post " : latetst_post}

# # Endpoint: Fetch a specific post by its unique ID
# @app.get("/post/{post_id}") 
# def fetch_post(*, post_id: int = Path(..., description="ID of the post to retrieve"),
# response : Response):

#     with pool.connection() as conn:
#         with conn.cursor() as cursor:
#             cursor.execute(""" SELECT * FROM posts WHERE post_id = %s """, (post_id,))
#             post = cursor.fetchone()
#             if not post:
#                 raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with the ID: {post_id} was not found")
#             return post

# #Endpoint: Delete the post with the given ID
# @app.delete("/post/{post_id}", status_code = status.HTTP_204_NO_CONTENT)
# def delete_post(post_id : int ):
#     with pool.connection() as conn:
#         with conn.cursor() as cursor :
#             cursor.execute(""" DELETE FROM posts WHERE post_id = %s RETURNING * """, (post_id,))
#             deleted_post = cursor.fetchone()
#             conn.commit()
#     if deleted_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the ID: {post_id} was not found")
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

# #Endpoint: Update post with the given ID
# @app.put("/post/{post_id}")
# def update_post(post_id : int, post : Post):

#     with pool.connection() as conn:
#         with conn.cursor() as cursor:
#             cursor.execute(""" UPDATE posts SET title = %s, content = %s, published = %s WHERE post_id = %s RETURNING * """, (post.title, post.content, post.published, post_id))
#             updated_post = cursor.fetchone()
#             conn.commit()
#     if updated_post is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with the ID: {post_id} was not found")
#     return {"data" : updated_post}
