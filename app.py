'''
__author__ == 'yyiust'
'''
from flask import Flask, make_response
app = Flask(__name__)
app.config.from_object('config')


@app.route('/book/search/<q>/<page>')
def search(q, page):
    """
        q: keyword/isbn
        page
    :return:
    """
    # isbn: isbn13: 13 digits
    # isbn10: 10digits and '-'
    isbn_or_key = 'key'
    if len(q) == 13 and q.isdigit():
        isbn_or_key = 'isbn'
    short_q = q.replace('-', '')
    if '-' in q and len(short_q) == 10 and short_q.isdigit():
        isbn_or_key = 'isbn'

    pass

# @app.route('/')
# def hello_world():
#     headers = {
#         'content-type': 'text/html'
#     }
#     response = make_response('<html></html>', 404)
#     response.headers = headers
#     # class-based view
#     return response

# app.add_url_rule('/', view_func=hello_world)
# app.run(debug=app.config['DEBUG'])
if __name__ == '__main__':
    # only run in this file, if this file is imported as module, will not execute
    # production environment, need use nginx + uwsgi(web server)
    # ensure this will not run in production environment
    app.run(debug=app.config['DEBUG'])
