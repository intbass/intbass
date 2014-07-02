import sys
import os
import logging
dir = os.path.dirname(os.path.abspath(__file__))
activate_this = '%s/bin/activate_this.py' % dir
execfile(activate_this, dict(__file__=activate_this))
#logging.basicConfig(filename='/home/intlbass/logs/flask.log')
#logger = logging.getLogger()
sys.path.insert(0, dir)
from app import app as application
#application.logger.addHandler(logger)
