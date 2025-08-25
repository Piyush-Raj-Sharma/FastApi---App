from fastapi import APIRouter, Depends, status, HTTPException, Response
from SQLALCHMY.orm import Session
from ..database import get_db
from .. import schemas, models

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.user.email == user_credentials.email).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, details=f"Invalid Credentials")