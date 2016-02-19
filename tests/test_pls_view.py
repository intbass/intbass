from tests.bass_test import BassTestCase
from app import db
from app.models import Mount, Station, Server
import tests
from logging import warn, info


TAG = 'example'
ENC = 'mp3'
QUAL = 'hi'
TITLE = 'example radio'
URL = 'http://localhost/{}-{}-{}'.format(TAG, ENC, QUAL)


class TestPlaylistView(BassTestCase):
    def test_empty(self):
        resp = self.app.get('/pls/example-mp3-hi')
        assert resp.status_code == 200
        warn(resp.data)
        assert '[playlist]' in resp.data
        assert 'numberofentries=0' in resp.data

    def test_unpublished(self):
        station = tests.station(name='intbass')
        db.session.add(station)
        server = tests.server()
        info(server.id)
        db.session.add(server)
        db.session.commit()
        db.session.add(tests.mount(server=server, station=station))
        db.session.commit()
        resp = self.app.get('/pls/intbass-mp3-hi')
        assert resp.status_code == 200
        assert 'numberofentries=0' in resp.data

    def assert_stream(self, idx, url, title):
        assert 'File{}={}'.format(idx, url) in self.pls
        assert 'Title{}={}'.format(idx, title) in self.pls
        assert 'Length{}=-1'.format(idx) in self.pls

    def test_success(self):
        station = tests.station(tag=TAG)
        db.session.add(station)
        server = tests.server()
        info(server.id)
        db.session.add(server)
        db.session.commit()
        db.session.add(tests.mount(title=TITLE, url=URL,
                                   station=station, server=server,
                                   published=True))
        db.session.commit()
        resp = self.app.get('/pls/{}-{}-{}'.format(TAG, ENC, QUAL))
        info(resp.data)
        self.pls = resp.data
        assert resp.status_code == 200
        assert 'numberofentries=1' in resp.data
        self.assert_stream(1, URL, TITLE)

    def test_success_two(self):
        title1 = 'example 1 radio'
        url1 = 'http://stream1.example/{}-{}-{}'.format(TAG, ENC, QUAL)
        title2 = 'example 2 radio'
        url2 = 'http://stream2.example/{}-{}-{}'.format(TAG, ENC, QUAL)
        station = tests.station(tag=TAG)
        db.session.add(station)
        server = tests.server()
        info(server.id)
        db.session.add(server)
        db.session.commit()
        db.session.add(tests.mount(title=title1, url=url1, preference=0,
                                   station=station, server=server,
                                   published=True))
        db.session.add(tests.mount(title=title2, url=url2, preference=1,
                                   station=station, server=server,
                                   published=True))
        db.session.commit()
        resp = self.app.get('/pls/{}-{}-{}'.format(TAG, ENC, QUAL))
        info(resp.data)
        self.pls = resp.data
        assert resp.status_code == 200
        assert 'numberofentries=2' in resp.data
        self.assert_stream(1, url1, title1)
        self.assert_stream(2, url2, title2)

    def test_filter_qual(self):
        title1 = 'example 1 radio'
        url1 = 'http://stream1.example/{}-{}-{}'.format(TAG, ENC, QUAL)
        title2 = 'example 2 radio'
        url2 = 'http://stream2.example/{}-{}-{}'.format(TAG, 'lo', QUAL)
        title3 = 'example 3 radio'
        url3 = 'http://stream3.example/{}-{}-{}'.format(TAG, ENC, QUAL)
        station = tests.station(tag=TAG)
        db.session.add(station)
        server = tests.server()
        db.session.add(server)
        db.session.commit()
        db.session.add(tests.mount(title=title1, url=url1, preference=0,
                                   station=station, server=server,
                                   published=True))
        db.session.add(tests.mount(title=title2, url=url2, preference=1,
                                   station=station, server=server,
                                   published=True))
        db.session.add(tests.mount(title=title3, url=url3, preference=2,
                                   station=station, server=server,
                                   published=True))
        db.session.commit()
        resp = self.app.get('/pls/{}-{}-{}'.format(TAG, ENC, QUAL))
        info(resp.data)
        self.pls = resp.data
        assert resp.status_code == 200
        assert 'numberofentries=2' in resp.data
        self.assert_stream(1, url1, title1)
        self.assert_stream(2, url3, title3)
