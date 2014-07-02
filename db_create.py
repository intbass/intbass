#!bin/python
from migrate.versioning import api
from app import app, db, validate
from app.models import Users
import os.path
import sys
from getpass import getpass
from gettext import gettext as _

affirmative = ['y', 'yes']


def colon(prompt):
    return '{}: '.format(prompt)


def question(prompt, options=None):
    if options is not None:
        options = ' ({})'.format('/'.join(options))
    return '{}{}? '.format(_('Continue'), options)


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


while True:
    name = input(colon(_('Admin username')))
    try:
        validate.username(name)
    except AssertionError as args:
        print _('Invalid username')
        continue
    break

while True:
    email = input(colon(_('Admin email address')))
    try:
        validate.email(email)
    except AssertionError as args:
        print _('Invalid email address')
        continue
    break

password = ''
confirm = 'no'
while password != confirm:
    password = getpass(prompt=colon(_('Admin password')))
    try:
        validate.password(password)
    except AssertionError:
        continue
    confirm = getpass(prompt=colon(_('Confirm admin password')))

confirm = input(question(_('Continue'), affirmative))
if confirm.lower() not in affirmative:
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
db.session.add(Users(name=name, location=_('Earth'),
                     email=email, password=password))
db.session.commit()
print _('Complete')
