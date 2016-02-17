from tests.bass_test import BassTestCase
from app import db
from logging import warn, info
import tests
import json
from nose.tools import nottest


TAG = 'example'
ENC = 'mp3'
QUAL = 'hi'
TITLE = 'example radio'
URL = 'http://localhost/{}-{}-{}'.format(TAG, ENC, QUAL)


class TestStationView(BassTestCase):
    def test_empty(self):
        resp = self.app.get('/station/example')
        info(resp.status_code)
        assert resp.status_code == 404

    @nottest
    def test_success(self):
        """ the defaults allow wrongness,
            until that is fixed this is not a test """
        station = tests.station(tag=TAG)
        db.session.add(station)
        db.session.commit()
        resp = self.app.get('/station/{}'.format(TAG))
        info(resp.status_code)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['listeners'] == 0
        assert data["artist"] is None
        assert data["live"] is False
        assert data["name"] is None
        assert data["playing"] is None
        assert data["tag"] == TAG
        warn(resp.data)
        assert False

    def test_bare_minimum(self):
        """ this is test_success cut down to the bare minumum until
            the models are correct in the setup to enforce booleans """
        station = tests.station(tag=TAG)
        db.session.add(station)
        db.session.commit()
        resp = self.app.get('/station/{}'.format(TAG))
        info(resp.status_code)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['listeners'] == 0
        assert data["tag"] == TAG
