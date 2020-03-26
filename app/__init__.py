"""
author: yyi
The initialization work for app.
"""
from flask import Flask
from app.models.book import db


def create_app():
    app = Flask(__name__, static_folder='static')
    app.config.from_object('app.secure')
    app.config.from_object('app.setting')
    register_blueprint(app)

    db.init_app(app)
    # db.create_all(app=app)
    # another way:
    with app.app_context():
        db.create_all()
    return app


def register_blueprint(app):
    from app.web.book import web
    # from app.web.user import user
    app.register_blueprint(web)



