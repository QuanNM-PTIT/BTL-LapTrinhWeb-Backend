from fastapi import APIRouter, Depends, HTTPException, status

import database
from JWTtoken import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from database import get_db
from sqlalchemy.orm import Session
from datetime import timedelta
from hashing import Hash
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
import models
import JWTtoken

router = APIRouter(
    tags=['Auth']
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post('/login')
async def login(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == request.username).first()
    if not user or not Hash.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail='Thông tin đăng nhập không chính xác.')
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "role": user.role}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/get_current_user')
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    return JWTtoken.verify_token(token, credentials_exception)
