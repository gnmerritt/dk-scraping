import json
import requests


class DKPlayerGroupFetcher(object):
    URL = "https://www.draftkings.com" + \
        "/lineup/getavailableplayers?draftGroupId={dgid}"

    def __init__(self, draft_group_id):
        self.url = self.URL.format(dgid=draft_group_id)

    def data(self):
        r = requests.get(self.url)
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
        return [DKPlayerAdder(p).generalize()
                for p in raw_players]


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
