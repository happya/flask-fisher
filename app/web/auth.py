"""

"""
# from app.forms.auth import RegisterForm, LoginForm, EmailForm, ResetPasswordForm, \
#     ChangePasswordForm
# from app.models.base import db
# from app.models.user import User
# from flask import render_template, request, redirect, url_for, flash
# from flask_login import login_user, logout_user, current_user, login_required
# from app.libs.email import send_mail
from . import web



@web.route('/register', methods=['GET', 'POST'])
def register():
    pass


@web.route('/login', methods=['GET', 'POST'])
def login():
    pass


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