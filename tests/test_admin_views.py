from tests.admin_test import AdminTestCase
from tests.bass_test import BassTestCase
from tests.user_test import UserTestCase


class TestAnonAdminView(BassTestCase):
    def test_admin_index(self):
        rv = self.app.get('/admin/')
        assert rv.status_code == 404

    def test_users_index(self):
        rv = self.app.get('/admin/users/')
        assert rv.status_code == 404

class TestUserAdminView(UserTestCase, TestAnonAdminView):
    pass

class TestAdminView(AdminTestCase):
    def test_users_index(self):
        rv = self.app.get('/admin/users/')
        assert rv.status_code == 200
        assert '<a href="/admin/users/edit/1">admin</a>' in rv.data
