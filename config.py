import os
basedir = os.path.abspath(os.path.dirname(__file__))

CSRF_ENABLED = True  # reduce request forgery
DEBUG = True         # production danger
FILE_PATH = os.path.join(basedir, 'local/Music')  # where to find audio files
GITHUB_INSTALL = 'http://github.com/'  # buildhooks blueprint; public github
HOST = '::'                            # local server bind; ipv6 & ipv4
HOSTNAME = 'localhost'                 # needed?
SECRET_KEY = 'My Super Secret key'     # Encryption
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
VERIFY_EMAIL_ADDRESSES = False
