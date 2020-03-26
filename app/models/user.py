"""
author: yyi
model: book
"""
# sqlalchemy
# Flask_SQLAlchemy
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash

from app import login_manager
from app.libs.helper import is_isbn_or_key
from app.models.base import Base
from app.models.gift import Gift
from app.models.wish import Wish
from app.spider.fish_book import FishBook


class User(UserMixin, Base):
    id = Column(Integer, primary_key=True)
    nickname = Column(String(24), nullable=False)
    _password = Column('password', String(128), nullable=False)
    phone_number = Column(String(18), unique=True)
    email = Column(String(50), unique=True, nullable=False)
    confirmed = Column(Boolean, default=False)
    beans = Column(Float, default=0)
    send_counter = Column(Integer, default=0)
    receive_counter = Column(Integer, default=0)
    wx_open_id = Column(String(50))
    wx_name = Column(String(32))

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, raw):
        self._password = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self._password, raw)
    # MVC M model only has data = data table
    # ORM

    # # for flask_login manager
    # def get_id(self):
    #     return self.id

    def can_save_to_list(self, isbn):
        # check if isbn is valid
        if is_isbn_or_key(isbn) != 'isbn':
            return False
        # check if can find book results
        fish_book = FishBook()
        fish_book.search_by_isbn(isbn)
        if not fish_book.first:
            return False
        # check if already in gift list
        # cannot send same book at the same time
        gifting = Gift.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        # check if user is a requester for this book
        # cannot be sender and receiver at the same time
        wishing = Wish.query.filter_by(uid=self.id, isbn=isbn,
                                       launched=False).first()
        return not gifting and not wishing

@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
