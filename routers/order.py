from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.orm.collections import InstrumentedList
from sqlalchemy.sql import exists

from database import get_db
import schemas
import models
from . import authentication

router = APIRouter(
    prefix='/order',
    tags=['Orders']
)


@router.post('/new_order')
def new_order(order: schemas.OrderCreate, db: Session = Depends(get_db),
              current_user: schemas.ShowUser = Depends(authentication.get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()

    cart = user.cart

    if isinstance(cart, InstrumentedList):
        cart = cart[0]

    new_order = models.Order(
        user_id=user.user_id,
        address=order.address,
        phone_number=order.phone_number,
        order_date=order.order_date,
        status=order.status
    )

    for detail in order.order_details:
        new_order_detail = models.OrderDetail(
            book_id=detail.book_id,
            quantity=detail.quantity,
            price=detail.price
        )
        new_order.order_details.append(new_order_detail)

        cart_detail = db.query(models.CartDetail).filter(
            models.CartDetail.cart_id == cart.cart_id,
            models.CartDetail.book_id == detail.book_id
        ).first()

        cart.cart_detail.remove(cart_detail)
        db.commit()

    db.add(new_order)
    db.query(models.CartDetail).filter(models.CartDetail.cart_id == None).delete()
    db.commit()

    return {"message": "Đặt hàng thành công!"}


@router.get('/all_order')
def get_all_order(db: Session = Depends(get_db),
                  current_user: schemas.ShowUser = Depends(authentication.get_current_user)):
    user = db.query(models.User).filter(models.User.email == current_user.email).first()

    orderList = []

    orders = db.query(models.Order).filter(models.Order.user_id == user.user_id).all()

    for order in orders:
        orderList.append({
            "user_id": user.user_id,
            "address": order.address,
            "order_date": order.order_date,
            "id": order.id,
            "phone_number": order.phone_number,
            "status": order.status,
            "user_name": order.user.name
        })

    return orderList


@router.get('/get_all_order_by_admin')
def get_all_order_by_admin(db: Session = Depends(get_db),
                  current_user: schemas.ShowUser = Depends(authentication.get_current_user)):
    if current_user.role != 'Admin':
        return

    orderList = []

    orders = db.query(models.Order).all()

    for order in orders:
        orderList.append({
            "user_id": order.user_id,
            "address": order.address,
            "order_date": order.order_date,
            "id": order.id,
            "phone_number": order.phone_number,
            "status": order.status,
            "user_name": order.user.name
        })

    return orderList


@router.get('/get_total_paid/{id}')
def get_total_paid(id: int, db: Session = Depends(get_db)):
    order_details = db.query(models.OrderDetail).filter(models.OrderDetail.order_id == id).all()

    total = 0
    for order_detail in order_details:
        total += order_detail.quantity * order_detail.price

    return {'total_paid': total}


@router.put('/change_status')
def change_status(request: schemas.OrderChangeStatus, db: Session = Depends(get_db)):
    order = db.query(models.Order).filter(models.Order.id == request.order_id).first()

    order.status = request.status
    db.commit()
    db.refresh(order)

    return {'status': 'Thay đổi trạng thái đơn hàng thành công!'}


@router.get('/get_order/{order_id}')
def get_order(order_id: int, db: Session = Depends(get_db)):
    return db.query(models.Order).filter(models.Order.id == order_id).first()


@router.get('/get_order_books/{order_id}')
def get_order_books(order_id: int, db: Session = Depends(get_db)):
    order_details = db.query(models.OrderDetail).filter(models.OrderDetail.order_id == order_id).all()

    order = db.query(models.Order).filter(models.Order.id == order_id).first()

    books = []

    for order_detail in order_details:
        books.append(schemas.CartItem(
            id=order_detail.book.id,
            user_id=order.user.user_id,
            title=order_detail.book.title,
            author=order_detail.book.author,
            category=order_detail.book.category,
            description=order_detail.book.description,
            num_pages=order_detail.book.num_pages,
            release_date=order_detail.book.release_date,
            price=order_detail.book.price,
            quantity=order_detail.quantity,
            image=order_detail.book.image
        ))

    return books


@router.get('/get_order_detail/{id}')
def get_order_detail(id: int, db: Session = Depends(get_db)):
    reviewed_book_ids = db.query(models.Review.book_id).subquery()

    order_details = db.query(models.OrderDetail).filter(
        models.OrderDetail.order_id == id,
        ~exists().where(
            (models.OrderDetail.book_id == reviewed_book_ids.c.book_id) &
            (models.OrderDetail.order_id == id)
        )
    ).all()

    return order_details
