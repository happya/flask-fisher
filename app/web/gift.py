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
from flask import current_app, flash, redirect, url_for, render_template
from flask_login import login_required, current_user
from . import web
from app.models.gift import Gift
from app.models.base import db
from app.view_models.gift import MyGifts


@web.route('/my/gifts')
@login_required
def my_gifts():
    uid = current_user.id
    # get all gifts uploaded by current user
    gifts_of_mine = Gift.get_user_gifts(uid)
    # get the isbn list of all these books
    isbn_list = [gift.isbn for gift in gifts_of_mine]
    # use "mysql in" to search the results in wishes
    wish_count_list = Gift.get_wish_counts(isbn_list)

    gifts_view_model = MyGifts(gifts_of_mine, wish_count_list)
    return render_template('my_gifts.html', gifts=gifts_view_model.gifts)


@web.route('/gifts/book/<isbn>')
@login_required
def save_to_gifts(isbn):
    '''
    check if isbn valid
    check if book exists
    :param isbn:
    :return:
    '''
    if current_user.can_save_to_list(isbn):
        # transaction
        # enable consistency
        # rollback
        # try:
        with db.auto_commit():
            # here the code is what do after yield
            gift = Gift()
            gift.isbn = isbn
            gift.uid = current_user.id
            current_user.beans += current_app.config['BEANS_UPLOAD_ONE_BOOK']
            db.session.add(gift)

            # db.session.commit()
        # except Exception as e:
        #     db.session.rollback()
        #     raise e
    else:
        flash('already added to your wish list or gift list!')
    return redirect(url_for('web.book_detail', isbn=isbn))


@web.route('/gifts/<gid>/redraw')
# @login_required
def redraw_from_gifts(gid):
    pass
