"""
author: yyi
"""
from flask import flash, url_for, redirect, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import or_, desc

from . import web
from app.forms.book import DriftForm
from ..libs.email import send_mail
from ..libs.enums import PendingStatus
from ..models.base import db
from ..models.drift import Drift
from ..models.gift import Gift
from ..models.user import User
from ..models.wish import Wish
from ..view_models.book import BookViewModel
from ..view_models.drift import DriftCollection


@web.route('/drift/<int:gid>', methods=['GET', 'POST'])
@login_required
def send_drift(gid):
    current_gift = Gift.query.get_or_404(gid)
    if current_gift.is_yourself_gift(current_user.id):
        flash('This book is yours. Cannot request book from yourself')
        return redirect(url_for('web.book_detail', isbn=current_gift.isbn))
    can = current_user.can_send_drift()
    if not can:
        return render_template('not_enough_beans.html', beans=current_user.beans)

    # form validation
    form = DriftForm(request.form)
    if request.method == 'POST' and form.validate():
        save_drift(form, current_gift)
        # remind the user: email
        send_mail(current_gift.user.email, 'Someone Wants A Book', 'email/get_gift.html',
                  wisher=current_user,
                  gift=current_gift)
        return redirect(url_for('web.pending'))

    # get current user summary
    gifter = current_gift.user.summary
    return render_template('drift.html',
                           gifter=gifter, user_beans=current_user.beans, form=form)


@web.route('/pending')
@login_required
def pending():
    # query Drift table
    drifts = Drift.query.filter(
        or_(Drift.requester_id == current_user.id,
            Drift.gifter_id == current_user.id
            )
    ).order_by(
        desc(Drift.create_time)
    ).all()
    views = DriftCollection(drifts, current_user.id)
    return render_template('pending.html', drifts=views.data)


# only gifter can reject
@web.route('/drift/<int:did>/reject')
@login_required
def reject_drift(did):
    with db.auto_commit():
        drift = Drift.query.filter(
            Gift.uid == current_user.id,
            Drift.id == did
        ).first_or_404()
        drift.pending = PendingStatus.Reject
        requester = User.query.get_or_404(drift.requester_id)
        requester.beans += 1
    return redirect(url_for('web.pending'))


# withdraw
@web.route('/drift/<int:did>/redraw')
@login_required
def redraw_drift(did):
    # 超权
    # uid :1  did:1
    # uid :2  did:2
    # should verify that current user's did matches the parameter did
    with db.auto_commit():
        drift = Drift.query.filter_by(
            requester_id=current_user.id,
            id=did
        ).first_or_404()
        drift.pending = PendingStatus.Withdraw
        current_user.beans += 1
    return redirect(url_for('web.pending'))


@web.route('/drift/<int:did>/mailed')
@login_required
def mailed_drift(did):
    # current user is the gifter
    with db.auto_commit():
        drift = Drift.query.filter_by(
            gifter_id=current_user.id,
            id=did
        )
        drift.pending = PendingStatus.Success
        current_user.beans += 1
        gift = Gift.query.filter_by(
            id=drift.gift_id
        ).first_or_404()
        gift.launched = True

        # update wish
        # Wish.query.filter_by(
        #     isbn=drift.isbn,
        #     uid=drift.requester_id,
        #     launched=False
        # ).update({Wish.launched: True})
        wish = Wish.query.filter_by(
            isbn=drift.isbn,
            uid=drift.requester_id,
            launched=False
        ).first()
        wish.launched = True
    return redirect(url_for('web.pending'))


def save_drift(drift_form, current_gift):
    """
    Instantiate a Drift,
    populate the properties from the submitted form to the model
    :param drift_form: The form submitted by user
    :param current_gift: Gift
    :return:
    """
    with db.auto_commit():
        drift = Drift()
        # mail info
        drift_form.populate_obj(drift)

        # dirft info
        drift.gift_id = current_gift.id
        drift.requester_id = current_user.id
        drift.requester_nickname = current_user.nickname
        drift.gifter_nickname = current_gift.user.nickname
        drift.gifter_id = current_gift.user.id

        # book info
        book = BookViewModel(current_gift.book)
        drift.book_title = book.title
        drift.book_author = book.author
        drift.book_img = book.image
        drift.isbn = book.isbn

        # transaction
        current_user.beans -= 1

        # database update
        db.session.add(drift)
