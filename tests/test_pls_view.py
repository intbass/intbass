from tests.bass_test import BassTestCase
from app import db
from app.models import Mount, Station, Server
from logging import warn, info


class TestPlaylistView(BassTestCase):
    def station(*args, **kwargs):
        defaults = {
            'tag': None,
            'name': None,
            'playing': None,
            'artist': None,
            'live': None
            }
        defaults.update(kwargs)
        return Station(**defaults)

    def server(*args, **kwargs):
        defaults = {
            'name': None,
            'host': None,
            'port': None,
            'user': None,
            'word': None
            }
        defaults.update(kwargs)
        return Server(**defaults)

    def mount(*args, **kwargs):
        defaults = {
            'station': None,
            'server': None,
            'info': None,
            'genre': None,
            'count': None,
            'peak': None,
            'max': None,
            'public': None,
            'slow': None,
            'url': None,
            'source': None,
            'start': None,
            'title': None,
            'bytesread': None,
            'bytessent': None,
            'published': None,
            'preference': None,
            'useragent': None
            }
        defaults.update(kwargs)
        assert defaults['server'] is not None
        assert defaults['station'] is not None
        return Mount(**defaults)

    def test_empty(self):
        resp = self.app.get('/pls/intbass-mp3-hi')
        assert resp.status_code == 200
        warn(resp.data)
        assert '[playlist]' in resp.data
        assert 'numberofentries=0' in resp.data

    def test_unpublished(self):
        station = self.station(name='intbass')
        db.session.add(station)
        server = self.server()
        info(server.id)
        db.session.add(server)
        db.session.commit()
        db.session.add(self.mount(server=server, station=station))
        db.session.commit()
        resp = self.app.get('/pls/intbass-mp3-hi')
        assert resp.status_code == 200
        assert 'numberofentries=0' in resp.data

    def assert_stream(self, idx, url, title):
        assert 'File{}={}'.format(idx, url) in self.pls
        assert 'Title{}={}'.format(idx, title) in self.pls
        assert 'Length{}=-1'.format(idx) in self.pls

    def test_success(self):
        tag = 'example'
        enc = 'mp3'
        qual = 'hi'
        title = 'example radio'
        url = 'http://localhost/{}-{}-{}'.format(tag, enc, qual)
        station = self.station(tag=tag)
        db.session.add(station)
        server = self.server()
        info(server.id)
        db.session.add(server)
        db.session.commit()
        db.session.add(self.mount(title=title, url=url,
                                  station=station, server=server,
                                  published=True))
        db.session.commit()
        resp = self.app.get('/pls/{}-{}-{}'.format(tag, enc, qual))
        info(resp.data)
        self.pls = resp.data
        assert resp.status_code == 200
        assert 'numberofentries=1' in resp.data
        self.assert_stream(1, url, title)

    def test_success_two(self):
        tag = 'example'
        enc = 'mp3'
        qual = 'hi'
        title1 = 'example 1 radio'
        url1 = 'http://stream1.example/{}-{}-{}'.format(tag, enc, qual)
        title2 = 'example 2 radio'
        url2 = 'http://stream2.example/{}-{}-{}'.format(tag, enc, qual)
        station = self.station(tag=tag)
        db.session.add(station)
        server = self.server()
        info(server.id)
        db.session.add(server)
        db.session.commit()
        db.session.add(self.mount(title=title1, url=url1, preference=0,
                                  station=station, server=server,
                                  published=True))
        db.session.add(self.mount(title=title2, url=url2, preference=1,
                                  station=station, server=server,
                                  published=True))
        db.session.commit()
        resp = self.app.get('/pls/{}-{}-{}'.format(tag, enc, qual))
        info(resp.data)
        self.pls = resp.data
        assert resp.status_code == 200
        assert 'numberofentries=2' in resp.data
        self.assert_stream(1, url1, title1)
        self.assert_stream(2, url2, title2)

    def test_filter_qual(self):
        tag = 'example'
        enc = 'mp3'
        qual = 'hi'
        title1 = 'example 1 radio'
        url1 = 'http://stream1.example/{}-{}-{}'.format(tag, enc, qual)
        title2 = 'example 2 radio'
        url2 = 'http://stream2.example/{}-{}-{}'.format(tag, 'lo', qual)
        title3 = 'example 3 radio'
        url3 = 'http://stream3.example/{}-{}-{}'.format(tag, enc, qual)
        station = self.station(tag=tag)
        db.session.add(station)
        server = self.server()
        db.session.add(server)
        db.session.commit()
        db.session.add(self.mount(title=title1, url=url1, preference=0,
                                  station=station, server=server,
                                  published=True))
        db.session.add(self.mount(title=title2, url=url2, preference=1,
                                  station=station, server=server,
                                  published=True))
        db.session.add(self.mount(title=title3, url=url3, preference=2,
                                  station=station, server=server,
                                  published=True))
        db.session.commit()
        resp = self.app.get('/pls/{}-{}-{}'.format(tag, enc, qual))
        info(resp.data)
        self.pls = resp.data
        assert resp.status_code == 200
        assert 'numberofentries=2' in resp.data
        self.assert_stream(1, url1, title1)
        self.assert_stream(2, url3, title3)
