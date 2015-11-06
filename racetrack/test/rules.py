from flask.ext.testing import TestCase

from racetrack.app import app, db


class AppTestCase(TestCase):
    def create_app(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite://"
        app.config['TESTING'] = True
        return app

    def setUp(self):
        self.db = db
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
