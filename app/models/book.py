"""
author: yyi
model: book
"""
# sqlalchemy
# Flask_SQLAlchemy


from sqlalchemy import Column, Integer, String
from flask_sqlalchemy import SQLAlchemy

from app.models.base import Base


class Book(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(50), nullable=False)
    author = Column(String(30), default="JohnDoe")
    binding = Column(String(20))
    publisher = Column(String(50))
    price = Column(String(20))
    pages = Column(Integer)
    pubdate = Column(String(20))
    isbn = Column(String(15), nullable=False, unique=True)
    summary = Column(String(1000))
    image = Column(String(50))

    # MVC M model only has data = data table
    # ORM

