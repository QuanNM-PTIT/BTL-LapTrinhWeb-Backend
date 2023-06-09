from sqlalchemy import Column, Integer, String, ForeignKey, DATE, Text
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'Users'

    user_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100))
    email = Column(String(100), index=True)
    password = Column(String(1000))
    role = Column(String(100), default='User')
    reviews = relationship("Review", back_populates="user")
    orders = relationship("Order", back_populates="user")
    cart = relationship("Cart", back_populates="user")


class Book(Base):
    __tablename__ = "Books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(1000))
    author = Column(String(1000))
    category = Column(String(100))
    description = Column(String(5000))
    num_pages = Column(Integer)
    release_date = Column(DATE)
    price = Column(Integer)
    image = Column(Text(length=2**31-1))
    reviews = relationship("Review", back_populates="book")
    order_details = relationship("OrderDetail", back_populates="book")
    cart_details = relationship("CartDetail", back_populates="book")


class Review(Base):
    __tablename__ = "Reviews"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"))
    book_id = Column(Integer, ForeignKey("Books.id"))
    rating = Column(Integer)
    comment = Column(String(5000))
    user = relationship("User", back_populates="reviews")
    book = relationship("Book", back_populates="reviews")


class Order(Base):
    __tablename__ = "Orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"))
    address = Column(String(1000))
    phone_number = Column(String(100))
    order_date = Column(String(100))
    status = Column(String(100))
    user = relationship("User", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")


class OrderDetail(Base):
    __tablename__ = "OrderDetails"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("Orders.id"))
    book_id = Column(Integer, ForeignKey("Books.id"))
    quantity = Column(Integer)
    price = Column(Integer)
    order = relationship("Order", back_populates="order_details")
    book = relationship("Book", back_populates="order_details")


class Cart(Base):
    __tablename__ = "Carts"

    cart_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("Users.user_id"))
    user = relationship("User", back_populates="cart")
    cart_detail = relationship("CartDetail", back_populates="cart")


class CartDetail(Base):
    __tablename__ = "CartDetails"

    cart_detail_id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("Carts.cart_id"))
    book_id = Column(Integer, ForeignKey("Books.id"))
    quantity = Column(Integer)
    cart = relationship("Cart", back_populates="cart_detail")
    book = relationship("Book", back_populates="cart_details")
