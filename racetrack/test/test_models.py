from rules import AppTestCase

from racetrack.app import db
from racetrack.app.models import Player, ExternalPlayer, Matchup, Projection


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


class ProjectionTest(AppTestCase):
    def fake_data(self, player, id, site):
        return {
            "matchup_id": id,
            "site": site,
            "player_id": player.id,
            "salary": 1000,
            "points": 22.5
        }

    def test_create_or_replace(self):
        tim = PlayerTest().add_player()
        data = self.fake_data(tim, 1, "DK")
        first = Projection.create_or_replace(data)
        self.assertEqual(tim.id, first.player_id)
        self.assertEqual(1000, first.salary)
        self.db.session.add(first)
        self.db.session.flush()

        data['salary'] = 2500
        second = Projection.create_or_replace(data)
        self.assertEqual(tim.id, second.player_id)
        self.assertEqual(first.site, second.site)
        self.assertEqual(2500, second.salary)
        self.db.session.add(second)
        self.db.session.commit()

        self.assertEqual(1, Projection.query.count())
