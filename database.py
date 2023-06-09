from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib.parse

# Tạo URL kết nối cơ sở dữ liệu
MYSQL_DATABASE_URL = "sqlite:///./sql_app.sqlite3"

engine = create_engine(
    MYSQL_DATABASE_URL, connect_args={"check_same_thread": False}
)

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()
