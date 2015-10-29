import unittest

import racetrack.scrapers.draftkings as dk


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
        players = dk.DKPlayerGroupFetcher(10)
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
