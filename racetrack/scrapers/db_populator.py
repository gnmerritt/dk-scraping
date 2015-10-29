from racetrack.app.models import Player, ExternalPlayer


class DbPopulator(object):
    """Split an iterable of generic players into players
    and external id objects"""
    KEYS = ["first", "last", "position", "sport"]

    def __init__(self, db):
        self.db = db
        self.player_to_externals = {}
        self.db_players = []

    def build_players(self, players):
        for p in players:
            db_player = self.__db_player(p)
            self.player_to_externals[db_player] = p
            self.db_players.append(db_player)

    def commit_players(self):
        for p in self.db_players:
            self.db.session.add(p)
        self.db.session.commit()

    def commit_externals(self):
        for p in self.db_players:
            data = self.player_to_externals[p]
            self.db.session.add(self.ext_player(p, data))

    def __db_player(self, player):
        return Player(**{
            k: v for k, v in player.items()
            if k in self.KEYS
        })

    def ext_player(self, db_player, player):
        info = {k: v for k, v in player.items()
                if k not in self.KEYS}
        info['player_id'] = db_player.id
        return ExternalPlayer(**info)
