"""
author: yyi
"""
from flask import current_app
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from sqlalchemy.orm import relationship

from app.models.base import db, Base
from app.models.wish import Wish
from app.spider.fish_book import FishBook


class Gift(Base):
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

    @property
    def book(self):
        fish_book = FishBook()
        fish_book.search_by_isbn(self.isbn)
        return fish_book.first

    @classmethod
    def recent(cls):
        # chained calls
        # 1. only limit count of books displayed: limit()
        # 2. order by create time: order_by()
        # 3. eliminate duplicates: group_by isbn, and distinct()
        recent_gift = Gift.query.filter_by(launched=False).group_by(
            Gift.isbn
        ).order_by(
            desc(Gift.create_time)
        ).limit(
            current_app.config['RECENT_BOOK_COUNT']
        ).distinct().all()
        return recent_gift

    @classmethod
    def get_user_gifts(cls, uid):
        """
        return all the gifts uploaded by current user
        :param uid: user id
        :return: a list of Gift with descend order of create time
        """
        return Gift.query.filter_by(
            uid=uid, launched=False
        ).order_by(
            desc(Gift.create_time)
        ).all()


    @classmethod
    def get_wish_counts(cls, isbn_list):
        """
        With the given isbn list, search Wish table to get a gift's wish counts
        :param isbn_list: a list of isbn
        :return: a list of number of wish counts of each isbn
        """
        # condition expression
        count_list = db.session.query(func.count(Wish.id), Wish.isbn).filter(
            Wish.launched == False,
            Wish.isbn.in_(isbn_list),
            Wish.status == 1
        ).group_by(
            Wish.isbn
        ).all()
        # change tuple to dict
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list


