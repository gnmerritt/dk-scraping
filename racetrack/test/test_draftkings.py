import unittest

import racetrack.scrapers.draftkings as dk

import mocks as m


class DKContestFetcherTest(unittest.TestCase):
    FILE = "/Users/nathan/sources/horses/data/dk_nfl_contests.json"

    def data(self):
        with open(self.FILE, "r") as myfile:
            return myfile.read().replace('\n', '')

    def test_parse_groups(self):
        contests = dk.DKContestFetcher()
        contests.data = self.data
        groups = contests.get_draft_groups()
        self.assertEqual([7579, 7623, 7624, 7625, 7626, 7627], groups)


class DKPlayerFetcherTest(unittest.TestCase):
    FILE = "/Users/nathan/sources/horses/data/dk_draft_group_7462.json"

    def data(self):
        with open(self.FILE, "r") as myfile:
            return myfile.read().replace('\n', '')

    def test_url(self):
        players = dk.DKPlayerGroupFetcher(15)
        self.assertIn("?draftGroupId=15", players.url)

    def test_call_fails(self):
        players = dk.DKPlayerGroupFetcher(10)
        players.url = "http://gaakjsdflj.com"
        try:
            players.data()
        except:
            pass
        else:
            self.fail("Bad request didn't explode")

    def test_parse_players(self):
        players = dk.DKPlayerGroupFetcher(10, checker=m.MockPlayerChecker)
        players.data = self.data
        player_data = players.load_data(limit=10)
        self.assertEqual(10, len(player_data))
        for p in players.parse_players(player_data):
            self.assertPlayer(p)

    def assertPlayer(self, obj):
        self.assertIn("first", obj)
        self.assertIn("last", obj)
        self.assertIn("position", obj)
        self.assertIn("external_id", obj)
        self.assertEqual(obj["site"], "DK")
        self.assertEqual(obj["sport"], "NFL")


class DKPlayerAdderTest(unittest.TestCase):
    def test_player_adder(self):
        raw_obj = {
            "pid": 22,
            "fn": "Tom",
            "ln": "Brady",
            "pn": "QB"
        }
        general = dk.DKPlayerAdder(raw_obj).generalize()
        self.assertEqual(22, general["external_id"])
        self.assertEqual("Tom", general["first"])
        self.assertEqual("Brady", general["last"])
        self.assertEqual("QB", general["position"])
        self.assertEqual("DK", general["site"])
        self.assertEqual("NFL", general["sport"])


class DKMatchupExtractorTest(unittest.TestCase):
    RAW = {
        "IsDisabledFromDrafting": False,
        "atabbr": "Atl",  # away team abbrv
        "atid": 323,      # away team id
        "htabbr": "Ten",    # home team abbrv.
        "htid": 336,        # home team id
        "pid": 456614,     # player id, used in lineups
        "pn": "WR",        # fantasy position
        "pp": 0,         # current score?
        "ppg": "25.3",    # PPG projection
        "s": 9100,       # salary": $9,100
        "tid": 323,    # player's team id
    }

    def test_disabled(self):
        logic = dk.DKMatchupExtractor({
            "IsDisabledFromDrafting": True
        }, "2015-09-02")
        self.assertFalse(logic.generalize())

    def test_generalize(self):
        logic = dk.DKMatchupExtractor(self.RAW, "2015-09-02")
        gen = logic.generalize()
        self.assertEqual(456614, gen['external_id'])
        self.assertEqual('DK', gen['site'])
        self.assertFalse(gen['home_game'])
        self.assertEqual("Atl", gen['team'])
        self.assertEqual("Ten", gen['opponent'])
        self.assertEqual(9100, gen['salary'])
        self.assertEqual("25.3", gen['points'])
