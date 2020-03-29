"""
author: yyi
"""
from sqlalchemy import Column, Integer, Boolean, ForeignKey, String, desc, func
from sqlalchemy.orm import relationship

from app.models.base import db, Base

from app.spider.fish_book import FishBook


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

    @property
    def book(self):
        fish_book = FishBook()
        fish_book.search_by_isbn(self.isbn)
        return fish_book.first

    @classmethod
    def get_user_wishes(cls, uid):
        """
        return all the wishes requested by current user
        :param uid: user id
        :return: a list of Wish with descend order of create time
        """
        return Wish.query.filter_by(
            uid=uid, launched=False
        ).order_by(
            desc(Wish.create_time)
        ).all()

    @classmethod
    def get_gifts_counts(cls, isbn_list):
        """
        With the given isbn list, search Wish table to get a gift's wish counts
        :param isbn_list: a list of isbn
        :return: a list of number of wish counts of each isbn
        """
        # condition expression
        count_list = db.session.query(func.count(Gift.id), Gift.isbn).filter(
            Gift.launched == False,
            Gift.isbn.in_(isbn_list),
            Gift.status == 1
        ).group_by(
            Gift.isbn
        ).all()
        # change tuple to dict
        count_list = [{'count': w[0], 'isbn': w[1]} for w in count_list]
        return count_list


from app.models.gift import Gift