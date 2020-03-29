"""
author: yyi
The initialization work for app.
"""
from flask import Flask
from app.models.base import db
from flask_login import LoginManager
from flask_mail import Mail

login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    db.init_app(app)
    # init login_manager
    login_manager.init_app(app)
    # define login view_function from end_point
    login_manager.login_view = 'web.login'
    login_manager.login_message = 'please login in or sign up'

    # init mail
    mail.init_app(app)

    # db.create_all(app=app)
    # another way:
    with app.app_context():
        db.create_all()
    return app


def register_blueprint(app):
    from app.web.book import web
    # from app.web.user import user
    app.register_blueprint(web)



