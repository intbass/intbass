from tests.bass_test import BassTestCase
from app.models import Users, UserCapabilities
from app import db

USERNAME = 'user'
PASSWORD = 'password'
EMAIL = 'user@example.com'
LOCATION = 'Venus'


class UserTestCase(BassTestCase):
    def login(self, username, password):
        return self.app.post('/login', data=dict(
            username=username,
            password=password
        ), follow_redirects=True)

    def logout(self):
        return self.app.get('/logout', follow_redirects=True)

    def setUp(self):
        super(UserTestCase, self).setUp()
        user = Users(name=USERNAME, location=LOCATION,
                      email=EMAIL, password=PASSWORD)
        db.session.add(user)
        db.session.commit()
        db.session.add(UserCapabilities(userid=user.id, capability='user'))
        db.session.commit()
        rv = self.login(USERNAME, PASSWORD)
        assert 'Welcome, {}'.format(USERNAME) in rv.data

    def tearDown(self):
        rv = self.logout()
        assert 'You have been successfully logged out' in rv.data
        super(UserTestCase, self).tearDown()
