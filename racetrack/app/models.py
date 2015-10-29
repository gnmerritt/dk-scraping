import datetime

from . import db


class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)  # eg 9738
    created = db.Column(db.DateTime)

    first = db.Column(db.String(40))
    last = db.Column(db.String(40))
    position = db.Column(db.String(10))  # e.g. 'WR'
    sport = db.Column(db.String(10))  # e.g. 'NFL'

    def __init__(self, first, last, position, sport):
        self.first = first
        self.last = last
        self.position = position
        self.sport = sport
        self.created = datetime.datetime.utcnow()

    def __repr__(self):
        return "Player(id={id}, name={f} {l}, pos={p})" \
            .format(id=self.id, f=self.first, l=self.last, p=self.position)


class ExternalPlayer(db.Model):
    __tablename__ = "external_players"
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), index=True)
    external_id = db.Column(db.String(40))
    site = db.Column(db.String(5))  # e.g. 'DK'

    primary_key = db.PrimaryKeyConstraint(player_id, site)

    def __init__(self, player_id, external_id, site):
        self.player_id = player_id
        self.external_id = external_id
        self.site = site

    def __repr__(self):
        return "ExtPlayer(id={id}, ext_id={eid}, site={s})" \
            .format(id=self.player_id, eid=self.external_id, s=self.site)


# Dictionary for lineups.
    # eg  14 / 201510261010 / 'Chargers' / 'NFL'
class Lineup(db.Model):
    __tablename__ = "lineups"

    id = db.Column(db.Integer, primary_key=True)  # eg 14
    created = db.Column(db.DateTime)

    # eg jockeyjz; associated with either of our DK/FD/.. profiles
    entryname = db.Column(db.String(100))

    team = db.Column(db.String(100))  # eg 'Steelers'
    sport = db.Column(db.String(10))  # eg 'NFL'

    def __repr__(self):
        return "Lineup(id={id}, team={t}, sport={s})" \
            .format(id=self.id, t=self.team, s=self.sport)


class ExternalLineup(db.Model):  # these are all historical
    """Dictionary for EXTERNAL lineups
    eg => [13,183801480,maxdalury (39/47),0,239.42,QB Andrew Luck
           RB Lamar Miller RB Todd Gurley WR Larry Fitzgerald
           WR Julio Jones WR T.Y. Hilton TE Crockett Gillmore]
    """
    __tablename__ = "external_lineups"

    # Import a lot of other people's lineups? OK with me.
    lineup_id = db.Column(db.Integer, db.ForeignKey("lineups.id"), index=True)
    # ['EntryId'] column from historical contest standings
    external_id = db.Column(db.Integer)
    site = db.Column(db.String(5))
    entryname = db.Column(db.String(140))  # eg 'maxdalury'

    team = db.Column(db.String(100))
    sport = db.Column(db.String(5))

    rel_rank = db.Column(db.Float)  # eg .0294859023 == top 3%
    contest = db.Column(db.Integer)  # contest id handed down from DK Api

    primary_key = db.PrimaryKeyConstraint(lineup_id, site)


class PlayerLineup(db.Model):  # actually a join... (vs Model?)
    """
    Join players and lineups.
    eg  9738 / 14 / 'WR'
    """
    __tablename__ = "playerlineups"

    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), index=True)
    # for internal or external lineups
    lineup_id = db.Column(db.Integer, db.ForeignKey("lineups.id"), index=True)

    player_position = db.Column(db.String(40))
    # in case player pos changes (Randy Moss plays WR and then TE or whatever).
    # nb QB Tom Brady RB Lamar Miller RB Todd Gurley WR Nate Washington
    #    WR Julio Jones WR Mike Evans TE Ladarius Green FLEX Rob

    primary_key = db.PrimaryKeyConstraint(player_id, lineup_id)

    def __repr__(self):
        return "PlayerLineup(player_id={p}, line_id={l}, player_position={pos})" \
            .format(id=self.player_id, l=self.line_id,
                    pos=self.player_position)
