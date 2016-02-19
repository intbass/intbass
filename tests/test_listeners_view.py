from tests.bass_test import BassTestCase
from app import db
from logging import warn, info
import tests
import json


TAG = 'example'
ENC = 'mp3'
QUAL = 'hi'
TITLE = 'example radio'
URL = 'http://localhost/{}-{}-{}'.format(TAG, ENC, QUAL)


class TestListenersView(BassTestCase):
    def test_empty(self):
        resp = self.app.get('/station/example/listeners')
        info(resp.status_code)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        assert data['max'] == 0
        assert 'data' in data
        assert len(data['data']) == 0

    def test_no_listeners(self):
        station = tests.station(tag=TAG)
        db.session.add(station)
        db.session.commit()
        resp = self.app.get('/station/{}/listeners'.format(TAG))
        info(resp.status_code)
        assert resp.status_code == 200
        data = json.loads(resp.data)
        warn(resp.data)
        assert data['max'] == 0
        assert 'data' in data
        assert len(data['data']) == 0

    def test_a_listener(self):
        station = tests.station(tag=TAG)
        db.session.add(station)
        server = tests.server()
        db.session.add(server)
        db.session.commit()
        mount = tests.mount(title=TITLE, url=URL,
                            station=station, server=server,
                            published=True)
        db.session.add(mount)
        db.session.commit()
        listener = tests.listener(mount=mount)
        listener.set_posn(0, 0)
        listener.seen()
        db.session.add(listener)
        db.session.commit()
        resp = self.app.get('/station/{}/listeners'.format(TAG))
        info(resp.status_code)

        assert resp.status_code == 200
        data = json.loads(resp.data)
        warn(resp.data)
        assert data['max'] == 1
        assert 'data' in data
        assert len(data['data']) == 1
