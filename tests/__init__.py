def assert_denied(r):
    assert r.status_code == 401
    assert r.headers.get('WWW-Authenticate') == 'None'
from app.models import Mount, Station, Server
from logging import warn, info


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
