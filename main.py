from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from routers import user, authentication, book, review, cart, order
from database import engine
import models

# Tạo các bảng trong cơ sở dữ liệu dựa trên định nghĩa trong models
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(authentication.router)
app.include_router(book.router)
app.include_router(review.router)
app.include_router(cart.router)
app.include_router(order.router)

# Thêm header Access-Control-Allow-Origin vào response header
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)