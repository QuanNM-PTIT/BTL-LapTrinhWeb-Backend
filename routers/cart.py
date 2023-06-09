from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.orm.collections import InstrumentedList

from database import get_db
import schemas
import models
from . import authentication

router = APIRouter(
    prefix='/cart',
    tags=['Carts']
)


@router.post('/add_cart')
def add_cart(request: schemas.CartCreate, db: Session = Depends(get_db),
             current_user: schemas.ShowUser = Depends(authentication.get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()

    cart = user.cart
    if not cart:
        cart = models.Cart(user_id=user.user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)

    if isinstance(cart, InstrumentedList):
        cart = cart[0]

    cart_detail = db.query(models.CartDetail).filter(models.CartDetail.cart_id == cart.cart_id,
                                                     models.CartDetail.book_id == request.book_id).first()

    if cart_detail:
        cart_detail.quantity += request.quantity
        db.commit()
    else:
        new_cart_detail = models.CartDetail(
            cart_id=cart.cart_id,
            book_id=request.book_id,
            quantity=request.quantity
        )
        db.add(new_cart_detail)
        db.commit()
        db.refresh(new_cart_detail)

    return {"message": "Thêm sách vào giỏ hàng thành công!"}


@router.get('/get_all_items')
def get_cart_items(db: Session = Depends(get_db),
                   current_user: schemas.ShowUser = Depends(authentication.get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()

    cart = user.cart

    if not cart:
        return {"message": "Giỏ hàng rỗng"}

    if isinstance(cart, InstrumentedList):
        cart = cart[0]

    cart_details = cart.cart_detail

    if not cart_details:
        return {"message": "Giỏ hàng rỗng"}

    books = []

    for cart_detail in cart_details:
        book = db.query(models.Book).get(cart_detail.book_id)
        item = schemas.CartItem(
            id=book.id,
            user_id=user.user_id,
            title=book.title,
            author=book.author,
            category=book.category,
            description=book.description,
            num_pages=book.num_pages,
            release_date=book.release_date,
            price=book.price,
            quantity=cart_detail.quantity,
            image=book.image
        )
        books.append(item)

    return {"message": "Thành công", "books": books}


@router.delete('/remove_item/{book_id}')
def remove_cart_item(book_id: int, db: Session = Depends(get_db),
                     current_user: schemas.ShowUser = Depends(authentication.get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    cart = user.cart

    if isinstance(cart, InstrumentedList):
        cart = cart[0]

    cart_detail = db.query(models.CartDetail).filter(
        models.CartDetail.cart_id == cart.cart_id,
        models.CartDetail.book_id == book_id
    ).first()

    cart.cart_detail.remove(cart_detail)
    db.commit()

    return {"message": "Xóa sách khỏi giỏ hàng thành công"}


@router.put('/edit_quantity')
def edit_quantity(request: schemas.EditQuantity, db: Session = Depends(get_db),
                  current_user: schemas.ShowUser = Depends(authentication.get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()
    cart = user.cart

    if isinstance(cart, InstrumentedList):
        cart = cart[0]

    cart_detail = db.query(models.CartDetail).filter(
        models.CartDetail.cart_id == cart.cart_id,
        models.CartDetail.book_id == request.book_id
    ).first()

    cart_detail.quantity = request.quantity

    db.commit()
    db.refresh(cart_detail)

    return {"message": "Cập nhật số lượng thành công!"}
