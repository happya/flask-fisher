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
from flask_login import login_user

from . import web
from app.forms.auth import RegisterForm, LoginForm
from app.models.user import User
from app.models.base import db


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
   pass


# 单元测试
@web.route('/reset/password/<token>', methods=['GET', 'POST'])
def forget_password(token):
    pass


@web.route('/change/password', methods=['GET', 'POST'])
# @login_required
def change_password():
    pass


@web.route('/logout')
def logout():
    pass