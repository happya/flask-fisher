"""
author: yyi
description: view function of Book
"""
import json
from flask import jsonify, request

from app.spider.fisher_book import FisherBook
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
        fisher_book = FisherBook()

        if isbn_or_key == 'isbn':
            fisher_book.search_by_keyword(q)
        else:
            fisher_book.search_by_keyword(q, page)

        books.fill(fisher_book, q)
        return json.dumps(books, default=lambda o: o.__dict__)
        # return json.dumps(result), 200, {'content-type': 'application/json'}
    else:
        return jsonify(form.errors)
