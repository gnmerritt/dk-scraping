from racetrack.app import db, app
from racetrack.scrapers import draftkings as dk
from racetrack.scrapers import db_populator


class AddPlayers(object):
    def __init__(self, db, logger):
        self.db = db
        self.logger = logger

    def run(self):
        self.logger.info("Scraping DK players and adding to DB")
        # hard-coded for now
        fetcher = dk.DKPlayerGroupFetcher("7594")
        raw_players = fetcher.load_data()
        self.logger.info(
            "Got {} players back from DK".format(len(raw_players)))
        players = fetcher.parse_players(raw_players)

        populator = db_populator.DbPopulator(self.db)
        populator.build_players(players)
        populator.commit_players()
        populator.commit_externals()

        return raw_players


class AddMatchupsProjections(object):
    def __init__(self, db, logger, raw_players):
        self.db = db
        self.logger = logger
        self.players = raw_players
        self.week = "2015-09-09"
        self.find_players()

    def find_players(self):
        finder = db_populator.PlayerFinder(
            self.db, self.players, 'DK', 'pid'
        )
        self.players_to_data = finder.map()

    def run(self):
        self.logger.info("Adding matchups and DK projections")
        matchups = {
            p.id: dk.DKMatchupExtractor(d, self.week).generalize()
            for p, d in self.players_to_data.items()
        }
        # Filter out invalid players
        matchups = {id: m for id, m in matchups.items() if m is not None}
        populator = db_populator.MatchupDbPopulator(self.db, matchups)
        populator.commit_matchups()
        populator.commit_projections()


if __name__ == "__main__":
    job = AddPlayers(db, app.logger)
    all_players = job.run()
    projections = AddMatchupsProjections(db, app.logger, all_players)
    projections.run()
