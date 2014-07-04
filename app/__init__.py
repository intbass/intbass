from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask('intbass')
app.config.from_object('config')
app.config.from_envvar("INTBASS_SETTINGS", silent=True)
app.root_path = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy(app)
lm = LoginManager()
lm.login_view = "login"
lm.init_app(app)

from app import views, models
lm.anonymous_user = models.AnonymousUser
