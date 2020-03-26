"""
author: yyi
The initialization work for Blueprint
"""
from flask import Blueprint

web = Blueprint('web', __name__)

from app.web import book, drift, wish, gift, main
from app.web import user
from app.web import auth