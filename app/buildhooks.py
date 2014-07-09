from flask import abort, Blueprint, request, Response
import json
from hashlib import sha256


class BuildHooksBlueprint(Blueprint):
    def register(self, app, options, first_registration=False):
        global auth
        self.app = app
        self.logger = app.logger

        super(BuildHooksBlueprint,
              self).register(app, options, first_registration)

    def config(self, key):
        return self.app.config.get(key)


buildhooks = app = BuildHooksBlueprint('buildhooks', __name__)


@app.route('/ci/travis', methods=['POST'])
def build_travis():
    token = app.config('TRAVIS_TOKEN')
    ghrepo = app.config('GITHUB_REPO')
    if token is None or ghrepo is None:
        app.logger.error('Travis-CI API options are not set')
        abort(500)
    auth = app.config('GITHUB_REPO') + app.config('TRAVIS_TOKEN')
    repo_url = app.config('GITHUB_INSTALL') + app.config('GITHUB_REPO')
    # Authenticate
    if sha256(auth).hexdigest() != request.headers.get('Authorization'):
        app.logger.info('Failed Travis CI authentication')
        abort(401)
    # Parse input
    try:
        note = json.loads(request.form['payload'].encode('ascii'))
    except ValueError:
        app.logger.critical('Failed travis-ci payload parsing')
        abort(400)
    # check if it is relevant
    if 'repository' not in note or note['repository'] is None:
        app.logger.warn('No repostory info in travis webhook')
        abort(400)
    # set a precondition of it matching the configured repo
    if note['repository']['url'] != repo_url:
        message = 'Not our repository: {}'.format(note['repository']['url'])
        app.logger.info(message)
        # HTTP Error 412 - Precondition failed
        # seems fair
        return Response(message, 412)

    # Do something?
    app.logger.info(json.dumps(note))

    message = note['status_message'] if 'status_message' in note else None
    if 'result_message' in note and message is None:
        message = note['result_message']
    if message is None:
        app.logger.warn('Travis webhook sent without any message')
        abort(400)
    return '{message}'.format(**note)
