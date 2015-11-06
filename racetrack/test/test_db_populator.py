import random
import string
import unittest

from racetrack.app import db
from racetrack.app.models import Player, ExternalPlayer
import racetrack.scrapers.db_populator as pop

from rules import AppTestCase
from test_models import PlayerTest
import mocks as m


def randomword(length):
    return ''.join(random.choice(string.ascii_lowercase)
                   for i in range(length))


class DbPopulatorTest(unittest.TestCase):
    def test_builder_players(self):
        db = m.MockDb()
        p = pop.DbPopulator(db)
        players = self.fake_players(15)
        p.build_players(players)
        self.assertEqual(15, len(p.db_players))
        self.assertEquals(15, len(p.player_to_externals))
        p.commit_players()
        self.assertEquals(p.db_players, db.session.added)

        db.session.added = []
        p.commit_externals()
        self.assertEquals(15, len(db.session.added))

    def test_ext_player(self):
        p = pop.DbPopulator(db=None)
        ext_player = p.ext_player(m.MockPlayer(), {
            'external_id': 'external',
            'site': 'the_site',
            'first': 'ignored',
            'sport': 'also hopefully ignored'
        })
        self.assertEqual('the_site', ext_player.site)
        self.assertEqual(1, ext_player.player_id)

    def fake_players(self, num):
        return [{
            'first': randomword(5),
            'last': randomword(8),
            'position': 'RB',
            'sport': 'NFL',
            'site': 'DK',
            'external_id': randomword(15)
        } for i in range(num)]


class PlayerExistsCheckTest(AppTestCase):
    def test_exists_doesnt(self):
        player = {'external_id': 1, 'site': 'DK'}
        check = pop.PlayerExistsCheck(player)
        self.assertFalse(check.exists())

    def test_exists_ext_id_match(self):
        pt = PlayerTest()
        pt.test_player_ext_player()
        player = {'external_id': "foo", 'site': 'DK'}
        check = pop.PlayerExistsCheck(player)
        self.assertTrue(check.exists())


class PlayerFinderTest(AppTestCase):
    def setUp(self):
        super().setUp()
        player = Player("F", "L", "QB", "NFL")
        db.session.add(player)
        db.session.flush()
        ext = ExternalPlayer(player.id, "foo", "DK", )
        db.session.add(ext)
        db.session.commit()

    def test_player_exists(self):
        finder = pop.PlayerFinder(db, [{'ext_id': 'foo'}], 'DK', 'ext_id')
        player = finder.map()
        self.assertEqual(1, len(player))

    def test_player_missing(self):
        finder = pop.PlayerFinder(db, [{'ext_id': 1}], 'DK', 'ext_id')
        player = finder.map()
        self.assertFalse(player)


class MatchupDbPopulatorTest(AppTestCase):
    def fake_player_map(self, num):
        return {
            i + 1: {
                'week': '2015-09-02',
                'home_game': False,
                'team': 'Ten',
                'opponent': 'Atl',
                'site': 'DK',
                'salary': 1000,
                'points': 15
            } for i in range(num)
        }

    def test_matchups(self):
        db = m.MockDb()
        players = self.fake_player_map(10)
        p = pop.MatchupDbPopulator(db, players)
        p.commit_matchups()
        self.assertEqual(10, len(db.session.added))

        db.session.added = []

        p.commit_projections()
        self.assertEqual(10, len(db.session.added))
        added = db.session.added[0]
        self.assertTrue(added.matchup_id)
