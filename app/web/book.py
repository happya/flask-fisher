"""
author: yyi
description: view function of Book
"""
from flask import jsonify, request, render_template, flash
from flask_login import current_user

from app.spider.fish_book import FishBook
from app.libs.helper import is_isbn_or_key

# blueprint
from . import web
from app.forms.book import SearchForm
from ..models.gift import Gift
from ..models.wish import Wish
from ..view_models.book import BookViewModel, BookCollection
from ..view_models.trade import TradeInfo


@web.route('/book/search')
def search():
    """
        q: keyword/isbn
        page
    :return:
    """
    # request.args: immutable dict
    # a = request.args.to_dict()

    # validation layer
    form = SearchForm(request.args)
    books = BookCollection()

    if form.validate():
        q = form.q.data.strip()
        page = form.page.data
        isbn_or_key = is_isbn_or_key(q)
        fisher_book = FishBook()

        if isbn_or_key == 'isbn':
            fisher_book.search_by_keyword(q)
        else:
            fisher_book.search_by_keyword(q, page)

        books.fill(fisher_book, q)
        # return json.dumps(books, default=lambda o: o.__dict__)

        # return json.dumps(result), 200, {'content-type': 'application/json'}
    else:
        flash('invalid search keyword')
        # return jsonify(form.errors)
    return render_template('search_result.html', books=books)


# book detail page
@web.route('/book/<isbn>/detail')
def book_detail(isbn):
    has_in_gifts = False
    has_in_wishes = False

    # get book details
    fish_book = FishBook()
    fish_book.search_by_isbn(isbn)
    book = BookViewModel(fish_book.first)

    # is current_user is the sender or requester of this book?
    # needs login
    if current_user.is_authenticated:
        # if is sender
        if Gift.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_gifts = True
        if Wish.query.filter_by(uid=current_user.id, isbn=isbn,
                                launched=False).first():
            has_in_wishes = True

    # get book as a gift, get all the sender
    trade_gifts = Gift.query.filter_by(isbn=isbn, launched=False).all()
    # get book as a wish, get all the requester
    trade_wishes = Wish.query.filter_by(isbn=isbn, launched=False).all()

    # get trade view model
    trade_gifts_model = TradeInfo(trade_gifts)
    trade_wishes_model = TradeInfo(trade_wishes)
    return render_template('book_detail.html', book=book,
                           wishes=trade_wishes_model,
                           gifts=trade_gifts_model,
                           has_in_gifts=has_in_gifts,
                           has_in_wishes=has_in_wishes)


@web.route('/test')
def test():
    r = {
        'name': 'Lionust',
        'age': 18
    }
    # data 关键字参数
    return render_template('test.html', data=r)
