"""
author: yyi
"""
from sqlalchemy import Column, Integer, String

from app.models.base import Base


class Drift(Base):
    """
        information for a transaction
    """
    id = Column(Integer, primary_key=True)
    # mail info
    recipient_name = Column(String(20), nullable=False)
    address = Column(String(100), nullable=False)
    message = Column(String(200))
    mobile = Column(String(20), nullable=False)

    # book info
    isbn = Column(String(13))
    book_title = Column(String(50))
    book_author = Column(String(30))
    book_img = Column(String(50))

    # requester info

