import datetime

from . import db


class Player(db.Model):
    __tablename__ = "players"
    id = db.Column(db.Integer, primary_key=True) # eg 9738
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


# Dictionary for lineups. 
    # eg  14 / 201510261010 / 'Chargers' / 'NFL' 
class Lineup(db.Model):
    __tablename__ = "lineups"
    
    id = db.Column(db.Integer, primary_key=True) # eg 14
    created = db.Column(db.DateTime)

    team = db.Column(db.String(100)) # eg 'Steelers'
    sport = db.Column(db.String(10)) # eg 'NFL'

    def __repr__(self):
        return "Lineup(id={id}, team={t}, sport={s})" \
            .format(id=self.id, t=self.team, s=self.sport)

    
    # Dictionary for EXTERNAL lineups # eg => [13,183801480,maxdalury (39/47),0,239.42,QB Andrew Luck RB Lamar Miller RB Todd Gurley WR Larry Fitzgerald WR Julio Jones WR T.Y. Hilton TE Crockett Gillmore]
    class ExternalLineup(db.Model):
        __tablename__ = "external_lineups"
        
        # site # eg 'DK'
        # entryname # eg 'maxdalury' => ie > real_slim_shady = 'maxdalury (39/47)'.split(' ').first
        # relative_rank # 13/2200 => .005905909090
        # contest # eg 12121321
        # 


# Join players and lineups. 
    # eg  9738 / 14 / 'WR'
class PlayerLineup(db.Model): # actually a join... (vs Model?)
    __tablename__ = "playerlineups"

    player_id = db.Column(db.Integer, db.ForeignKey("players.id"), index=True)
    line_id = db.Column(db.Integer, db.ForeignKey("lineups.id"), index=True) # for internal or external lineups

    player_position = db.Column(db.String(40)) # in case player pos changes (Randy Moss plays WR and then TE or whatever). not indexed on.
        # nb QB Tom Brady RB Lamar Miller RB Todd Gurley WR Nate Washington WR Julio Jones WR Mike Evans TE Ladarius Green FLEX Rob 

    def __repr__(self):
        return "PlayerLineup(player_id={p}, line_id={l}, player_position={pos})" \
            .format(id=self.player_id, l=self.line_id, pos=self.player_position)

