#!bin/python
from migrate.versioning import api
from app import app, db
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
db_repo = app.config['SQLALCHEMY_MIGRATE_REPO']
db_uri = app.config['SQLALCHEMY_DATABASE_URI']
if not os.path.exists(db_repo):
    api.create(db_repo, 'database db_repository')
    api.version_control(db_uri, db_repo)
else:
    api.version_control(db_uri, db_repo, api.version(db_repo))
admin = Users(name=name, location=_('Earth'), email=email)
admin.set_password(password)
db.session.add(admin)
db.session.commit()
print _('Complete')
