from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session

from database import get_db
import schemas
import models
from routers import authentication

router = APIRouter(
    prefix='/review',
    tags=['Reviews']
)


@router.post('/add_review')
def add_review(request: schemas.ReviewCreate, db: Session = Depends(get_db), current_user: schemas.ShowUser = Depends(authentication.get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()

    new_review = models.Review(user_id=user.user_id, book_id=request.book_id, rating=request.rating,
                               comment=request.comment)
    db.add(new_review)
    db.commit()
    db.refresh(new_review)
    return {'status': 'Thêm đánh giá thành công!'}


@router.get('/get_review/{id}')
def get_review(id: int, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.id == id).first()
    reviews_with_user = []
    for review in book.reviews:
        review_with_user = schemas.ReviewWithUser(
            id = review.id,
            rating=review.rating,
            comment=review.comment,
            user=review.user.name
        )
        reviews_with_user.append(review_with_user)

    return reviews_with_user
