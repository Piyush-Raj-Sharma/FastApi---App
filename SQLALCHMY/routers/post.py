from fastapi import FastAPI, HTTPException, Path, status, Depends, APIRouter
from ..database import get_db
from .. import models, schemas
from sqlalchemy.orm import Session

router = APIRouter()

@router.get("/orm-posts", response_model=list[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

@router.get("/orm-posts/latest", response_model = schemas.PostResponse)
def fetch_latest_post(db: Session = Depends(get_db)):
    post = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"Post not found")
    return post
    
@router.post("/orm-posts", response_model=schemas.PostResponse , status_code = status.HTTP_201_CREATED)  #when we CREATE something we should give 201_created status code
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):  
    new_post = models.Post(**post.dict())
    # new_post = models.Post(title=post.title, content=post.content, published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post) 
    return new_post

# Endpoint: Fetch a specific post by its unique ID
@router.get("/orm-posts/{post_id}", response_model=schemas.PostResponse) 
def fetch_post(*, post_id: int = Path(..., description="ID of the post to retrieve"),
db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.post_id == post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"post with the ID: {post_id} was not found")
    return post

#Endpoint: Update post with the given ID
@router.put("/orm-post/{post_id}", response_model = schemas.PostResponse)
def update_post(post_id : int, updated_post: schemas.PostUpdate, db: Session = Depends(get_db)):

    post_query = db.query(models.Post).filter(models.Post.post_id == post_id)
    post = post_query.first()

    if post is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f"post with the ID: {post_id} was not found")
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()


#Endpoint: Delete the post with the given ID
@router.delete("/orm-post/{post_id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(post_id : int, db: Session = Depends(get_db) ):
    post_query = db.query(models.Post).filter(models.Post.post_id == post_id)

    if not post_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with the ID: {post_id} was not found")
    post_query.delete(synchronize_session=False)
    db.commit()
    return None
