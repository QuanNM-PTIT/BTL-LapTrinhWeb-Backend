from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from typing import Optional


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class ShowUser(BaseModel):
    name: str
    email: str
    role: str

    class Config():
        orm_mode = True


class User(UserBase):
    user_id: int
    role: Optional[str]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    user_id: int
    role: Optional[str]

    class Config:
        orm_mode = True


class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None


class BookCreate(BaseModel):
    title: str
    author: str
    category: Optional[str]
    description: Optional[str]
    num_pages: Optional[int]
    release_date: date
    price: int
    image: str


class BookUpdate(BaseModel):
    title: str
    author: str
    category: Optional[str]
    description: Optional[str]
    num_pages: Optional[int]
    release_date: date
    price: int
    image: str


class ShowBook(BaseModel):
    id: int
    title: str
    author: str
    category: Optional[str]
    description: Optional[str]
    num_pages: Optional[int]
    release_date: date
    price: int
    image: str

    class Config:
        orm_mode = True


class ReviewCreate(BaseModel):
    book_id: int
    rating: int
    comment: str


class ReviewWithUser(BaseModel):
    id: int
    rating: int
    comment: str
    user: str

    class Config:
        orm_mode = True


class CartCreate(BaseModel):
    book_id: int
    quantity: int


class CartItem(BaseModel):
    id: int
    user_id: int
    title: str
    author: str
    category: Optional[str]
    description: Optional[str]
    num_pages: Optional[int]
    release_date: date
    price: int
    image: str
    quantity: int


class EditQuantity(BaseModel):
    book_id: int
    quantity: int


class OrderDetailCreate(BaseModel):
    book_id: int
    quantity: int
    price: int


class OrderCreate(BaseModel):
    address: str
    phone_number: str
    order_date: str
    status: str
    order_details: List[OrderDetailCreate]


class OrderChangeStatus(BaseModel):
    order_id: int
    status: str


class ShowOrder(BaseModel):
    id: int
    user_id: int
    address: str
    phone_number: str
    order_date: str
    status: str
