#!bin/python
from app import app
app.config.from_envvar("INTBASS_SETTINGS", silent=True)
app.run(host=app.config['HOST'])
