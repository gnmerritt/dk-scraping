import logging
import slacker_log_handler as slh

from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config.from_object('racetrack.app.default_settings')
app.config.from_envvar('RACETRACK_SETTINGS', silent=True)

db = SQLAlchemy(app)

if not app.debug:
    handler = slh.SlackerLogHandler(
        app.config['SLACK_API_KEY'],
        app.config['SLACK_CHANNEL'],
        username=app.config['SLACK_USERNAME']
    )
    handler.setLevel(logging.ERROR)
    app.logger.addHandler(handler)

from . import models
