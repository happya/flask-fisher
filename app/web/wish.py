"""

"""
# from flask import flash, redirect, url_for, render_template, request
# from flask.ext.login import current_user
#
# from app.libs.email import send_mail
# from app.models.base import db
# from app.models.gift import Gift
# from app.models.wish import Wish
# from app.view_models.trade import MyTrades
# from app import limiter
# from flask_login import login_required
from . import web



def limit_key_prefix():
    pass


@web.route('/my/wish')
def my_wish():
    pass

@web.route('/wish/book/<isbn>')
# @login_required
def save_to_wish(isbn):
    pass

@web.route('/satisfy/wish/<int:wid>')
# @limiter.limit(key_func=limit_key_prefix)
# @login_required
def satisfy_wish(wid):
    pass


@web.route('/wish/book/<isbn>/redraw')
# @login_required
def redraw_from_wish(isbn):
    pass


# @limiter.limited
def satifiy_with_limited():
    pass
