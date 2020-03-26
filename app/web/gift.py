"""

"""
# from app.libs.enums import PendingStatus
# from app.models.base import db
# from app.models.drift import Drift
# from app.models.gift import Gift
# from app.view_models.trade import MyTrades
# from . import web
# from flask import current_app, flash, redirect, url_for, render_template
# from flask_login import login_required, current_user

from . import web


@web.route('/my/gifts')
# @login_required
def my_gifts():
    pass


@web.route('/gifts/book/<isbn>')
# @login_required
def save_to_gifts(isbn):
    pass


@web.route('/gifts/<gid>/redraw')
# @login_required
def redraw_from_gifts(gid):
    pass
