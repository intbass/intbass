from tests.admin_test import AdminTestCase
from tests.bass_test import BassTestCase
from tests.user_test import UserTestCase


class TestAnonAdminView(BassTestCase):
    def test_denied(self):
        for url in '', 'users/', 'users/edit/1', 'files/', 'files/a':
            rv = self.app.get('/admin/{}'.format(url))
            assert rv.status_code == 404


class TestUserAdminView(UserTestCase, TestAnonAdminView):
    pass


class TestAdminView(AdminTestCase):
    def test_users_index(self):
        rv = self.app.get('/admin/users/')
        assert rv.status_code == 200
        assert '<a href="/admin/users/edit/1">admin</a>' in rv.data
