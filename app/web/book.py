"""
author: yyi
description: view function of Book
"""
from flask import jsonify

from fisher_book import FisherBook
from helper import is_isbn_or_key

# blueprint
from . import web


@web.route('/book/search/<q>/<page>')
def search(q, page):
    """
        q: keyword/isbn
        page
    :return:
    """
    isbn_or_key = is_isbn_or_key(q)
    if isbn_or_key == 'isbn':
        result = FisherBook.search_by_isbn(q)
    else:
        result = FisherBook.search_by_isbn(q)
    # return json.dumps(result), 200, {'content-type': 'application/json'}
    return jsonify(result)