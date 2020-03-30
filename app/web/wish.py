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
from flask import flash, redirect, url_for, render_template
from flask_login import login_required, current_user

from . import web
from ..libs.email import send_mail
from ..models.base import db
from ..models.gift import Gift
from ..models.wish import Wish
from ..view_models.trade import MyTrades
from ..view_models.wish import MyWishes


def limit_key_prefix():
    pass


@web.route('/my/wish')
def my_wish():
    uid = current_user.id
    # get current user's wishes
    wishes_of_mine = Wish.get_user_wishes(uid)
    # get the isbn list of all the wishes
    isbn_list = [wish.isbn for wish in wishes_of_mine]
    # get all the gift counts with the isbn of wishes
    gift_count_list = Wish.get_gifts_counts(isbn_list)
    wishes_view_model = MyTrades(wishes_of_mine, gift_count_list)
    return render_template('my_wish.html', wishes=wishes_view_model.trades)


@web.route('/wish/book/<isbn>')
@login_required
def save_to_wish(isbn):
    if current_user.can_save_to_list(isbn):
        with db.auto_commit():
            wish = Wish()
            wish.uid = current_user.id
            wish.isbn = isbn
            db.session.add(wish)
    else:
        flash('This book is already in your wish list or gift list!')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/satisfy/wish/<int:wid>')
# @limiter.limit(key_func=limit_key_prefix)
@login_required
def satisfy_wish(wid):
    # send book
    # some one wants a book
    wish = Wish.query.get_or_404(wid)
    # check if current user uploads this book as a gift
    gift = Gift.query.filter_by(
        uid=current_user.id,
        isbn=wish.isbn
    ).first()
    # if not a gift, should upload
    if not gift:
        flash('You have not uploaded this book. Please click Add to Gift. '
              'Please make sure your can send this book before add it to gift')
    # if uploaded, send the wisher an email
    else:
        send_mail(wish.user.email,
                  'Someone wants to send you a Book',
                  'email/satisfy_wish.html',
                  wish=wish, gift=gift)
        flash('An email is sent to the wisher. '
              'If he/she accepts your gift, your will receive a gift')
    return redirect(url_for('web.book_detail', isbn=wish.isbn))


@web.route('/wish/book/<isbn>/redraw')
@login_required
def redraw_from_wish(isbn):
    wish = Wish.query.filter_by(
        isbn=isbn,
        launched=False
    ).first()
    with db.auto_commit():
        wish.delete()
    return redirect(url_for('web.my_wish'))


# @limiter.limited
def satifiy_with_limited():
    pass
