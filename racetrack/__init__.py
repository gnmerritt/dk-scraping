from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('racetrack.default_settings')
app.config.from_envvar('RACETRACK_SETTINGS', silent=True)

db = SQLAlchemy(app)

from . import models
