import sys
import os
import logging
dir = os.path.dirname(os.path.abspath(__file__))
activate_this = '%s/bin/activate_this.py' % dir
execfile(activate_this, dict(__file__=activate_this))
#logging.basicConfig(filename='/home/intlbass/logs/flask.log')
#logger = logging.getLogger()
sys.path.insert(0, dir)
#application.logger.addHandler(logger)
# WSGI sends environmnet vairables on a per request basis in req_environ
def application(req_environ, start_response):
    os.environ['INTBASS_SETTINGS'] = req_environ['INTBASS_SETTINGS']
    from app import app
    return app(req_environ, start_response)
