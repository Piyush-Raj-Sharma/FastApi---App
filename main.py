from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

my_posts = [
    {
        "title": 1,
        "content" : "Learning FastAPI",
        "published" : True,
        "ratings" : "5 STAR"
    },
    {
        "title": 2,
        "content" : "Learned React/Redux",
        "published" : False,
        "ratings" : "4 STAR"
    }
]

class Post(BaseModel):
    title: int
    content: str
    published: bool = True
    ratings: Optional[str] = None

@app.get("/")
def root():
    return {"message" : "Hello from the social media app"}

@app.get("/post")
def get_posts():
    return my_posts