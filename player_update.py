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
        fetcher = dk.DKPlayerGroupFetcher("7462")
        raw_players = fetcher.load_data()
        players = fetcher.parse_players(raw_players)

        populator = db_populator.DbPopulator(self.db)
        populator.build_players(players)
        populator.commit_players()
        populator.commit_externals()


if __name__ == "__main__":
    job = AddPlayers(db, app.logger)
    job.run()
