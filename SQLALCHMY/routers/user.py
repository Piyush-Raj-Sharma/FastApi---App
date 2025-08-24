from fastapi import FastAPI, HTTPException, Path, status, Response, Depends, APIRouter
from ..database import get_db
from .. import models, schemas, utils
from sqlalchemy.orm import Session

router = APIRouter(
    prefix = "/users",
    tags = ['User'])

#Endpoint for creating Users
@router.post('/users', response_model=schemas.UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

#Endopoint for fetching all Users
@router.get('/', response_model=list[schemas.UserResponse])
def fetch_all_user(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users

#Endpoint for fetching specific Users
@router.get("/{user_id}", response_model=schemas.UserResponse)
def fetch_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , detail=f"user with the User_ID: {user_id} was not found")
    return user

#Endpoint for deleting Specific user
@router.delete('/{user_id}', status_code = status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session=Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.user_id == user_id)
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with the User_ID: {user_id} was not found")
    user_query.delete(synchronize_session=False)
    db.commit()
    return None

#Endpoint for updating User Data
@router.patch('/{user_id}', response_model=schemas.UserResponse)
def update_user(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    user_query = db.query(models.User).filter(models.User.user_id == user_id)
    db_user = user_query.first()

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with ID {user_id} was not found"
        )
    
    # Only update provided fields (exclude_unset ignores missing ones)
    user_data = user.dict(exclude_unset=True)
    for key, value in user_data.items():
        setattr(db_user, key, value)

    db.commit()
    db.refresh(db_user)
    return db_user


