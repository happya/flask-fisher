"""
author: yyi
model: book
"""
# sqlalchemy
# Flask_SQLAlchemy
from math import floor

from flask import current_app
from flask_login import UserMixin
from sqlalchemy import Column, Integer, String, Boolean, Float
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

from app import login_manager
from app.libs.enums import PendingStatus
from app.libs.helper import is_isbn_or_key
from app.models.base import Base, db
from app.models.drift import Drift
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

    def can_send_drift(self):
        """
        check if can send a drift
        1. can not request a book from self
        2. should have enough beans
        3. must send a book per requesting two books
        :return:
        """
        if self.beans < 1:
            return False
        # get the count of sent gifts
        success_gifts_count = Gift.query.filter_by(
            uid=self.id,
            launched=True
        ).count()
        # get the count of successfully requested book
        success_receive_count = Drift.query.filter_by(
            requester_id=self.id,
            pending=PendingStatus.Success
        ).count()
        return True if floor(success_receive_count / 2) <= floor(success_gifts_count) else False

    def generate_token(self, expiration=600):
        """
        generate token
        :param expiration: token lifetime, seconds
        :return:
        """
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'id': self.id}).decode('utf-8')

    @staticmethod
    def reset_password(token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token.encode('utf-8'))
        except:
            return False
        uid = data.get('id')
        with db.auto_commit():
            user = User.query.get(uid)
            user.password = new_password
        return True

    @property
    def summary(self):
        return dict(
            nickname=self.nickname,
            beans=self.beans,
            email=self.email,
            send_receive=str(self.send_counter) + '/' + str(self.receive_counter)
        )

@login_manager.user_loader
def get_user(uid):
    return User.query.get(int(uid))
