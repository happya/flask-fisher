"""
author: yyi
"""
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String
from sqlalchemy.orm import relationship

from app.models.base import db, Base


class Wish(Base):
    id = Column(Integer, primary_key=True)
    # user
    user = relationship('User')
    uid = Column(Integer, ForeignKey('user.id'))

    # isbn can represent book
    isbn = Column(String(15), nullable=False)
    # book
    # book = relationship('Book')
    # bid = Column(Integer, ForeignKey('book.id'))

    launched = Column(Boolean, default=False)

