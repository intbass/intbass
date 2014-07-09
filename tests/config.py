import os
basedir = os.path.abspath(os.path.dirname(__file__))

TESTING = True
WTF_CSRF_ENABLED = False
CSRF_ENABLED = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')

VERIFY_EMAIL_ADDRESSES = False
DEBUG = True
SECRET_KEY = 'My test key'
FILE_PATH = os.path.join(basedir, 'local/Music')
HOSTNAME = 'localhost'
HOST = '::'
GITHUB_REPO = 'my/repo'
TRAVIS_TOKEN = 'travis-key'
