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
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'],
                       convert_unicode=True)
sessionmaker(autocommit=False, autoflush=False, bind=engine)

lm = LoginManager()
lm.login_view = "login"
lm.init_app(app)
app.register_blueprint(buildhooks, url_prefix='/build')

from app import views, models
lm.anonymous_user = models.AnonymousUser
