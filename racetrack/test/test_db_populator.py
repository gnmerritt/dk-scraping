import random
import string
import unittest

import racetrack.scrapers.db_populator as pop

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
