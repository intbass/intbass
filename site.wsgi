import sys
import os
import logging
dir = os.path.dirname(os.path.abspath(__file__))
activate_this = '%s/bin/activate_this.py' % dir
execfile(activate_this, dict(__file__=activate_this))
sys.path.insert(0, dir)
# WSGI sends environment variables on a per request basis in req_environ
def application(req_environ, start_response):
    os.environ['INTBASS_SETTINGS'] = req_environ['INTBASS_SETTINGS']
    from app import app
    stdhandler = logging.StreamHandler(stream=sys.stderr)
    stdhandler.setLevel(logging.DEBUG)
    app.logger.addHandler(stdhandler)
    return app(req_environ, start_response)
