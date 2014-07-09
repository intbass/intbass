def assert_denied(r):
    assert r.status_code == 401
    assert r.headers.get('WWW-Authenticate') == 'None'
