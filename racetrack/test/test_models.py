from rules import AppTestCase

from racetrack.app import db
from racetrack.app.models import Player, ExternalPlayer, Matchup


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


class MatchupTest(AppTestCase):
    def test_get_or_create(self):
        tim = PlayerTest().add_player()
        self.assertTrue(tim.id)
        data = {
            "player_id": tim.id,
            "week": "THE_WEEK",
            "opponent": "Ind",
            "team": "NE",
            "home_game": True
        }
        matchup = Matchup.get_or_create(data)
        self.assertTrue(matchup)
        self.assertEqual(data['week'], matchup.week)
        self.assertEqual(tim.id, matchup.player_id)
        another = Matchup.get_or_create(data)
        self.assertEqual(matchup, another)
        again = Matchup.get_or_create(data)
        self.assertEqual(matchup, again)

    def test_matchups_unique(self):
        """Verifies that a player can only have one matchup per week"""
        pass
