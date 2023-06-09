from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import func
from sqlalchemy.orm import Session

from database import get_db
import schemas
import models
from . import authentication

router = APIRouter(
    prefix='/book',
    tags=['Books']
)


@router.get('/', response_model=List[schemas.ShowBook])
def get_all_book(db: Session = Depends(get_db)):
    books = db.query(models.Book).all()
    return [schemas.ShowBook.from_orm(book) for book in books]


@router.post('/new_book')
def add_book(request: schemas.BookCreate, db: Session = Depends(get_db),
             current_user: schemas.ShowUser = Depends(authentication.get_current_user)):
    if current_user.role != 'Admin':
        return

    existing_book = db.query(models.Book).filter(
        models.Book.title == request.title and models.Book.author == request.author).first()
    if existing_book:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Sách này đã tồn tại.")
    new_book = models.Book(**request.dict())
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return {"status": "Thêm sách thành công!"}


@router.get('/{id}')
def get_book_by_id(id: int, db: Session = Depends(get_db)):
    return db.query(models.Book).filter(models.Book.id == id).first()


@router.delete('/delete/{id}')
def delete_book(id: int, db: Session = Depends(get_db),
                current_user: schemas.ShowUser = Depends(authentication.get_current_user)):
    if current_user.role == 'User':
        return

    book = db.query(models.Book).filter(models.Book.id == id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Sách không tồn tại")
    db.delete(book)
    db.query(models.Review).filter(models.Review.book_id == None).delete()
    db.commit()
    return {"message": "Xóa sách thành công"}


@router.put('/update/{id}')
def update_book(id: int, book: schemas.BookUpdate, db: Session = Depends(get_db),
                current_user: schemas.ShowUser = Depends(authentication.get_current_user)):
    if current_user.role == 'User':
        return

    existing_book = db.query(models.Book).filter(models.Book.id != id, models.Book.title == book.title,
                                                 models.Book.author == book.author).first()

    if existing_book:
        raise HTTPException(status_code=400, detail="Sách đã tồn tại!")

    updated_book = db.query(models.Book).filter(models.Book.id == id).first()

    if not updated_book:
        raise HTTPException(status_code=404, detail="Sách không tồn tại.")

    for field, value in book.dict(exclude_unset=True).items():
        setattr(updated_book, field, value)

    db.commit()
    db.refresh(updated_book)
    return {"status": "Cập nhật sách thành công!"}


@router.get('/count_books/{id}')
def count_books_by_id(id: int, db: Session = Depends(get_db)):
    count = db.query(func.sum(models.OrderDetail.quantity)).join(models.OrderDetail.order).filter(
        models.OrderDetail.book_id == id,
        ~models.Order.status.in_(['Đã hủy', 'Chưa xác nhận'])
    ).scalar()
    if not count:
        count = 0
    return {'count': count}
