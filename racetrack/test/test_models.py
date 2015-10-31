from rules import AppTestCase

from racetrack.app import db
from racetrack.app.models import Player, ExternalPlayer


class PlayerTest(AppTestCase):
    def add_player(self):
        p = Player("Tim", "Brady", "QB", "NFL")
        db.session.add(p)
        db.session.commit()
        tim = Player.query.filter_by(first="Tim").first()
        self.assertTrue(tim.id)
        self.assertTrue(tim.created)
        self.assertEqual("Player(id=1, name=Tim Brady, pos=QB)", repr(tim))
        return tim

    def test_player_ext_player(self):
        tim = self.add_player()
        external = ExternalPlayer(tim.id, "foo", "DK")
        db.session.add(external)
        db.session.commit()
        from_db = ExternalPlayer.query.filter_by(site="DK").first()
        self.assertEqual(from_db.player_id, tim.id)
        self.assertEqual("foo", from_db.external_id)
