import os

DEBUG = True
SECRET_KEY = 'tia asset tracker!'
WTF_CSRF_ENABLED = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
    os.path.dirname(__file__), '../tia_db.sqlite3')
