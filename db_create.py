#!bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
from app.models import Users
import os.path


def input(prompt):
    # Fix Python 2.x.
    try:
        input = raw_input
    except NameError:
        pass

    value = ''
    while value == '':
        value = input('{}: '.format(prompt))
    return value


db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
admin = Users(name=input('Admin username'),
              location='Earth',
              email=input('Admin email address'),
              )
admin.set_password('password')
db.session.add(admin)
db.session.commit()
