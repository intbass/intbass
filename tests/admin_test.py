from tests.bass_test import BassTestCase
from app.models import Users, UserCapabilities
from app import db

USERNAME = 'admin'
PASSWORD = 'password'
EMAIL = 'admin@example.com'
LOCATION = 'Mars'


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
        admin = Users(name=USERNAME, location=LOCATION,
                      email=EMAIL, password=PASSWORD)
        db.session.add(admin)
        db.session.commit()
        db.session.add(UserCapabilities(userid=admin.id, capability='admin'))
        db.session.add(UserCapabilities(userid=admin.id, capability='user'))
        db.session.commit()
        rv = self.login(USERNAME, PASSWORD)
        assert 'Welcome, {}'.format(USERNAME) in rv.data

    def tearDown(self):
        rv = self.logout()
        assert 'You have been successfully logged out' in rv.data
        super(AdminTestCase, self).tearDown()
