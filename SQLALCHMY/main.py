from fastapi import FastAPI, HTTPException, Path, status, Response, Depends
from random import randrange 
from app.db import pool
from .database import Base, engine, get_db
from . import models, schemas, utils
from sqlalchemy.orm import Session
from .routers import auth, post, user


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


# -----------------------------------------------------------------------------


