import json

from racetrack.scrapers.db_populator import PlayerExistsCheck
from racetrack.scrapers.client import RequestWrapper


class DKPlayerGroupFetcher(object):
    URL = "https://www.draftkings.com" + \
        "/lineup/getavailableplayers?draftGroupId={dgid}"

    def __init__(self, draft_group_id, checker=PlayerExistsCheck):
        self.url = self.URL.format(dgid=draft_group_id)
        self.checker = checker

    def data(self):
        r = RequestWrapper().get(self.url)
        if r and r.text:
            return r.text
        raise ValueError("No data found for {}".format(self.url))

    def load_data(self, limit=None):
        data = self.data()
        json_data = json.loads(data)
        players = json_data['playerList']
        if limit is not None:
            return players[:limit]
        return players

    def parse_players(self, raw_players):
        general_players = [DKPlayerAdder(p).generalize()
                           for p in raw_players]
        new_players = [p for p in general_players
                       if not self.checker(p).exists()]
        return new_players


class DKPlayerAdder(object):
    MAP = {
        "pid": "external_id",
        "fn": "first",
        "ln": "last",
        "pn": "position"
    }
    DK_SITE_ID = "DK"

    def __init__(self, raw_data):
        self.raw = raw_data

    def generalize(self):
        g = {}
        for k, m in self.MAP.items():
            g[m] = self.raw[k]
        g["site"] = self.DK_SITE_ID
        g["sport"] = "NFL"
        return g
