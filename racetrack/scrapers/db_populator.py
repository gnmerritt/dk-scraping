from racetrack.app.models import Player, ExternalPlayer, Matchup, Projection


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
        self.db.session.commit()

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


class PlayerExistsCheck(object):
    """"Checks the DB to see if (external_id, site) exists"""
    def __init__(self, general_player):
        self.player = general_player

    def exists(self):
        return ExternalPlayer.query.filter_by(
            external_id=str(self.player['external_id']),
            site=self.player['site']
        ).count() > 0


class PlayerFinder(object):
    def __init__(self, db, raw_players, site, id_field):
        self.db = db
        self.players = raw_players
        self.site = site
        self.id_field = id_field

    def map(self):
        mapped = {}
        for p in self.players:
            db_player = self.db.session.query(Player.id) \
                .filter(
                    ExternalPlayer.external_id == str(p[self.id_field]),
                    ExternalPlayer.site == self.site
                ).outerjoin(ExternalPlayer) \
                .first()
            if db_player is not None:
                mapped[db_player] = p
        return mapped


class MatchupDbPopulator(object):
    """Adds matchups and site projections for players"""
    MATCHUP_KEYS = ['player_id', 'week', 'opponent', 'team', 'home_game']
    PROJECTION_KEYS = ['player_id', 'matchup_id', 'site', 'salary', 'points']

    def __init__(self, db, players_to_gen_data):
        self.db = db
        self.player_id_to_data = players_to_gen_data
        self.matchups = []

    def commit_matchups(self):
        for id, data in self.player_id_to_data.items():
            data['player_id'] = id
            matchup = self.for_matchup(data)
            row = Matchup(**matchup)
            self.db.session.add(row)
            self.db.session.flush()
            data['matchup_id'] = row.id
        self.db.session.commit()

    def for_matchup(self, data):
        return {
            k: v for k, v in data.items()
            if k in self.MATCHUP_KEYS
        }

    def commit_projections(self):
        for id, data in self.player_id_to_data.items():
            projection = self.for_projection(data)
            row = Projection(**projection)
            self.db.session.add(row)
        self.db.session.commit()

    def for_projection(self, data):
        return {
            k: v for k, v in data.items()
            if k in self.PROJECTION_KEYS
        }
