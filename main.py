from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

class post(BaseModel):
    title: int
    content: str
    published: bool = True
    ratings: Optional[str] = None

@app.get("/")
def root():
    return {"message" : "Hello from the social media app"}

