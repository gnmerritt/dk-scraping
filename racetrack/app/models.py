import datetime

from . import db


class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime)

    first = db.Column(db.String(40))
    last = db.Column(db.String(40))
    position = db.Column(db.String(10))  # e.g. 'WR'
    sport = db.Column(db.String(10))  # e.g. 'NFL'

    def __repr__(self):
        return "Player(id={id}, name={f} {l}, pos={p})" \
            .format(id=self.id, f=self.first, l=self.last, p=self.pos)


class ExternalPlayer(db.Model):
    __tablename__ = "external_players"
    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), index=True)
    external_id = db.Column(db.String(40))
    site = db.Column(db.String(5))  # e.g. 'DK'

    primary_key = db.PrimaryKeyConstraint(player_id, site)

    def __repr__(self):
        return "ExtPlayer(id={id}, ext_id={eid}, site={s})" \
            .format(id=self.player_id, eid=self.external_id, s=self.site)
