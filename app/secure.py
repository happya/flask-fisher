"""
author: yyi
1. confidential information such as password
2. different for development/production environment
not push to git
"""


DEBUG = True
SQLALCHEMY_DATABASE_URI = 'mysql+cymysql://root:Sql&2333@localhost:3306/fisher' # cymysql: driver, needs install
SQLALCHEMY_TRACK_MODIFICATIONS = True
SECRET_KEY = b'_5#y2L"F4Q8z/'

# Email config
MAIL_SERVER = 'smtp.gmail.com'
MAIL_USE_SSL = True
MAIL_USE_TLS = False
MAIL_PORT = 465
MAIL_USERNAME = 'lionust001@gmail.com'
MAIL_PASSWORD = 'ggbhdepngyovwlld'
