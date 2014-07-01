#!bin/python
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI
from config import SQLALCHEMY_MIGRATE_REPO
from app import db
from app.models import Users
import os.path
import sys
from getpass import getpass
from gettext import gettext as _

affirmative = ['y', 'yes']


def colon(prompt):
    return '{}: '.format(prompt)


def input(prompt):
    # Fix Python 2.x.
    try:
        input = raw_input
    except NameError:
        pass

    value = ''
    while value == '':
        value = input(prompt)
    return value


name = input(colon(_('Admin username')))
email = input(colon(_('Admin email address')))
password = ''
confirm = 'no'
while password != confirm:
    password = getpass(prompt=colon(_('Admin password')))
    confirm = getpass(prompt=colon(_('Confirm admin password')))

confirm = input('{} ({})? '.format(_('Continue'), '/'.join(affirmative))).lower()
if confirm not in affirmative:
    print _('Exiting')
    sys.exit()

db.create_all()
if not os.path.exists(SQLALCHEMY_MIGRATE_REPO):
    api.create(SQLALCHEMY_MIGRATE_REPO, 'database repository')
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
else:
    api.version_control(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, api.version(SQLALCHEMY_MIGRATE_REPO))
admin = Users(name=name, location=_('Earth'), email=email)
admin.set_password(password)
db.session.add(admin)
db.session.commit()
print _('Complete')
