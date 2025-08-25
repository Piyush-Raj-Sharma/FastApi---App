from fastapi import APIRouter, Depends, status, HTTPException, Response
from SQLALCHMY.orm import Session
from ..database import get_db
from .. import schemas

router = APIRouter(tags=['Authentication'])

@router.post('/login')
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
