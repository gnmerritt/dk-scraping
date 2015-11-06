import json

from racetrack.scrapers.db_populator import PlayerExistsCheck
from racetrack.scrapers.client import RequestWrapper


class DKContestFetcher(object):
    """Fetches all active DK contests, finds draft groups"""
    URL = "https://www.draftkings.com/lobby/getcontests?sport=NFL"

    def __init__(self):
        self.json_data = None

    def data(self):
        r = RequestWrapper().get(self.URL)
        if r and r.text:
            return r.text
        raise ValueError("No data found for {}".format(self.URL))

    def load_data(self):
        data = self.data()
        self.json_data = json.loads(data)

    def get_draft_groups(self):
        if not self.json_data:
            self.load_data()
        draft_groups = self.json_data['DraftGroups']
        group_ids = [g.get("DraftGroupId", None)
                     for g in draft_groups]
        return [id for id in group_ids if id is not None]


class DKPlayerGroupFetcher(object):
    """Fetches all players in a DK draft group"""

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
    """Pulls out general player information from a DK player object"""

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


class DKMatchupExtractor(object):
    """Extracts a generalized matchup object given a DK player"""

    MAP = {
        "s": "salary",
        "ppg": "points",
        "pid": "external_id",
    }

    def __init__(self, raw, week):
        self.raw = raw
        self.week = week

    def generalize(self):
        """Returns a generalized matchup object"""
        if self.raw.get('IsDisabledFromDrafting', False):
            return None
        g = {m: self.raw[k] for k, m in self.MAP.items()}
        g['site'] = 'DK'
        g['week'] = self.week
        self.add_teams(g)
        return g

    def add_teams(self, general):
        """Calculates 'team', 'opponent' and 'home_game'"""
        home = self.raw['htabbr']
        away = self.raw['atabbr']
        is_home_game = self.raw['htid'] == self.raw['tid']
        general['home_game'] = is_home_game
        if is_home_game:
            general['team'] = home
            general['opponent'] = away
        else:
            general['opponent'] = home
            general['team'] = away
