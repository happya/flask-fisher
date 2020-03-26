"""
author: yyi
description: view function of Book
"""
import json
from flask import jsonify, request, render_template, flash

from app.spider.fish_book import FishBook
from app.libs.helper import is_isbn_or_key

# blueprint
from . import web
from app.forms.book import SearchForm
from ..view_models.book import BookViewModel, BookCollection


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
    fish_book = FishBook()
    fish_book.search_by_isbn(isbn)
    book = BookViewModel(fish_book.first)
    return render_template('book_detail.html', book=book, wishes=[], gifts=[])


@web.route('/test')
def test():
    r = {
        'name': 'Lionust',
        'age': 18
    }
    # data 关键字参数
    return render_template('test.html', data=r)
