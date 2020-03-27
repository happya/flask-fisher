"""
author: yyi
register form
"""
from wtforms import Form, StringField, PasswordField
from wtforms.validators import DataRequired, Length, Email, ValidationError

from app.models.user import User


class RegisterForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                        Email(message='invalid email address')])
    password = PasswordField(validators=[DataRequired(message='password must not be empty'), Length(6, 32)])
    nickname = StringField(validators=[DataRequired(), Length(2, 10, message="nickname must has length between 2-10")])

    def validate_email(self, field):
        """
        check if email exists
        :return:
        """
        if User.query.filter_by(email=field.data).first():
            raise ValidationError("email already exists!")

    def validate_nickname(self, field):
        if User.query.filter_by(nickname=field.data).first():
            raise ValidationError("nickname already exists!")


class LoginForm(Form):
    email = StringField(validators=[DataRequired(), Length(8, 64),
                                    Email(message='invalid email address')])
    password = PasswordField(validators=[DataRequired(message='password must not be empty'), Length(6, 32)])
