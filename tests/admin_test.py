# coding=utf8
from tests.bass_test import BassTestCase
from app.models import Users, UserCapabilities
from app import db

PRIMARY_USERNAME = 'admin'
PRIMARY_PASSWORD = 'password'
PRIMARY_EMAIL = 'admin@example.com'
PRIMARY_LOCATION = 'Mars'

SECONDARY_USERNAME = 'jupiter'
SECONDARY_PASSWORD = u'Diéspiter'
SECONDARY_EMAIL = 'jupiter@example.com'
SECONDARY_LOCATION = 'Juptier'


class AdminTestCase(BassTestCase):
    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def setUp(self):
        super(AdminTestCase, self).setUp()
        admin = Users(name=PRIMARY_USERNAME, location=PRIMARY_LOCATION,
                      email=PRIMARY_EMAIL, password=PRIMARY_PASSWORD)
        db.session.add(admin)
        admin2 = Users(name=SECONDARY_USERNAME, location=SECONDARY_LOCATION,
                       email=SECONDARY_EMAIL, password=SECONDARY_PASSWORD)
        db.session.add(admin2)
        db.session.commit()
        db.session.add(UserCapabilities(userid=admin.id, capability='admin'))
        db.session.add(UserCapabilities(userid=admin.id, capability='user'))
        db.session.add(UserCapabilities(userid=admin2.id, capability='admin'))
        db.session.add(UserCapabilities(userid=admin2.id, capability='user'))
        db.session.commit()
        rv = self.login(PRIMARY_USERNAME, PRIMARY_PASSWORD)
        assert 'Welcome, {}'.format(PRIMARY_USERNAME) in rv.data

    def tearDown(self):
        rv = self.logout()
        assert 'You have been successfully logged out' in rv.data
        super(AdminTestCase, self).tearDown()
