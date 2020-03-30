"""
validation layer for book viewfunction
"""
from wtforms import Form, StringField, IntegerField
from wtforms.validators import Length, NumberRange, DataRequired, Regexp


class SearchForm(Form):
    q = StringField(validators=[DataRequired(), Length(min=1, max=30)])
    page = IntegerField(validators=[NumberRange(min=1, max=99)], default=1)


class DriftForm(Form):
    recipient_name = StringField('Recipient',
                                 validators=[DataRequired(),
                                             Length(min=2, max=20,
                                                    message='The recipient name must have 2-20 characters')])
    mobile = StringField('Mobile', validators=[DataRequired(), Regexp('^1[0-9]{10}', 0,
                                                                      message='please input a valid mobile number')])
    message = StringField()
    address = StringField(validators=[DataRequired(),
                                      Length(10, 70, message='please input a valid address')])
