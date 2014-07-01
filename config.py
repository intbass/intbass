import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

DEBUG = True
CSRF_ENABLED = True
SECRET_KEY = 'My Super Secret key'
FILE_PATH = os.path.join(basedir, '/Music')
HOST = '0.0.0.0'
