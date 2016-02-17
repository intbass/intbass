from tests.bass_test import BassTestCase
from tests import assert_denied
from tests.fakes.travis import FakeTravisPayload
from logging import info

GOODAUTH = '7328c42cf38a08d22e5a650786d1965ab4c6c195c96abf8e4387249030c5b277'
BAADAUTH = '8328c42cf38a08d22e5a650786d1965ab4c6c195c96abf8e4387249030c5b278'


class TestTravisView(BassTestCase):
    def webhook(self, payload='', auth=GOODAUTH, url='/build/ci/travis'):
        info('Using Authorization: %s', auth)
        info('Submitting %s', payload)
        return self.app.post(url, data={'payload': payload},
                             headers={'Authorization': auth})

    def test_denied(self):
        rv = self.app.post('/build/ci/travis')
        assert_denied(rv)

    def test_empty_auth(self):
        resp = self.webhook(auth='')
        assert_denied(resp)

    def test_bad_auth(self):
        resp = self.webhook(auth=BAADAUTH)
        assert_denied(resp)

    def test_bad_json(self):
        resp = self.webhook(payload='bleigrh')
        assert resp.status_code == 400

    def test_empty_payload(self):
        resp = self.webhook(payload='{}')
        assert resp.status_code == 400

    def test_other_repo(self):
        payload = FakeTravisPayload(status=0, repo_owner='undef')
        resp = self.webhook(payload=payload)
        assert resp.status_code == 412

    def test_success(self):
        payload = FakeTravisPayload(status=0)
        resp = self.webhook(payload=payload)
        info(resp.data)
        assert resp.status_code == 200

    def test_fail(self):
        payload = FakeTravisPayload(status=99)
        resp = self.webhook(payload=payload)
        info(resp.data)
        assert resp.status_code == 200
