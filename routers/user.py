from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import schemas
import models
from hashing import Hash

router = APIRouter(
    prefix='/user',
    tags=['Users']
)


# @router.get('/', response_model=List[schemas.User])
# def get_all_user(db: Session = Depends(get_db)):
#     return db.query(models.User).all()


@router.post('/register')
def register(request: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.email == request.email).first()

    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Email đã tồn tại.')

    new_user = models.User(
        name=request.name,
        email=request.email,
        password=Hash.bcrypt(request.password)
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {'status': 'Đăng ký thành công'}


@router.get('/get_user_name/{id}')
def get_user_name(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.user_id == id).first()

    return {'user_name': user.name}