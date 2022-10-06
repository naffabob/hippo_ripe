from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Peer(db.Model):
    __tablename__ = "peers"
    id = db.Column(db.Integer, primary_key=True)
    asn = db.Column(db.String, unique=True, nullable=False)
    asset = db.Column(db.String, unique=False, nullable=True)
    client = db.Column(db.String, unique=False, nullable=True)
    prefixes = db.relationship("Prefix")

    def __repr__(self):
        return f'<Peer {self.asn}>'


class Prefix(db.Model):
    __tablename__ = "prefixes"
    id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.String, unique=False, nullable=False)
    peer = db.Column(db.Integer, db.ForeignKey("peers.id", ondelete="CASCADE"), nullable=False)

    def __repr__(self):
        return f'<Prefix {self.prefix}>'
