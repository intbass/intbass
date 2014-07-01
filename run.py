#!bin/python
from app import app
app.run(host=app.config['HOST'])
