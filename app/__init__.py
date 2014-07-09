from flask import Flask
from flask.ext.login import LoginManager
from flask.ext.sqlalchemy import SQLAlchemy
import os
from app.buildhooks import buildhooks

app = Flask('intbass')
app.config.from_object('config')
app.config.from_envvar("INTBASS_SETTINGS", silent=True)
app.root_path = os.path.abspath(os.path.dirname(__file__))
db = SQLAlchemy(app)
lm = LoginManager()
lm.login_view = "login"
lm.init_app(app)
app.register_blueprint(buildhooks, url_prefix='/build')

from app import views, models
lm.anonymous_user = models.AnonymousUser
