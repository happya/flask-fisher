"""

"""
# from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm, \
#     ChangePasswordForm
# from app.models.base import db
# from app.models.user import User
# from flask import render_template, request, redirect, url_for, flash
# from flask_login import login_user, logout_user, current_user, login_required
# from app.libs.email import send_mail
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from . import web
from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm
from app.models.user import User
from app.models.base import db
from ..libs.email import send_mail


@web.route('/register', methods=['GET', 'POST'])
def register():
    # request.form obtain submitted information
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        with db.auto_commit():
            user = User()
            user.set_attrs(form.data)
            db.session.add(user)
        # db.session.commit()
        return redirect(url_for('web.login'))
    return render_template('auth/register.html', form=form)


@web.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            # cookie
            # if remember=True, cookie 365 day; else, once
            login_user(user, remember=True)
            # get the url that needs to jump
            next = request.args.get('next')
            if not next or next.startswith('/'):
                next = url_for('web.index')
            return redirect(next)
        else:
            flash("user doesn't exist or invalid password")
    return render_template('auth/login.html', form=form)


@web.route('/reset/password', methods=['GET', 'POST'])
def forget_password_request():
    form = EmailForm(request.form)
    if request.method == 'POST':
        if form.validate():
            account_email = form.email.data
            try:
                user = User.query.filter_by(email=account_email).first_or_404()
                send_mail(account_email,
                          'Reset your password',
                          'email/reset_password.html',
                          user=user,
                          token=user.generate_token())
                flash('An email has been sent to ' + account_email + ' , please check your mailbox.')
                # return redirect(url_for('web.login'))
            except Exception as e:
                return render_template('404.html')
    return render_template('auth/forget_password_request.html', form=form)


# unit test
@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    form = ResetPasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        success = User.reset_password(token, form.password1.data)
        if success:
            flash('your password is successfully reset')
            return redirect(url_for('web.login'))
        else:
            flash('unable to reset your password')

    return render_template('auth/forget_password.html', form=form)


@web.route('/change/password', methods=['GET', 'POST'])
# @login_required
def change_password():
    pass


@web.route('/logout')
def logout():
    # clear cookies
    logout_user()
    return redirect(url_for('web.index'))
