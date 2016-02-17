from app import app, db
from tests import config
import unittest
from logging import warn


class BassTestCase(unittest.TestCase):
    """A base test case for international bass."""

    def setUp(self):
        warn('setup: {}'.format(self))
        app.config.from_object(config)
        self.app = app.test_client()
        db.create_all()
        warn('complete setup: {}'.format(self))

    def tearDown(self):
        db.session.remove()
        db.drop_all()


if __name__ == '__main__':
    unittest.main()
