from webapp.model_db import db


class Peer(db.Model):
    __tablename__ = "peers"
    id = db.Column(db.Integer, primary_key=True)
    asn = db.Column(db.String, unique=True, nullable=False)
    asset = db.Column(db.String, unique=False, nullable=True)
    remark = db.Column(db.String, unique=False, nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey("clients.id", ondelete="CASCADE"), nullable=True)
    client = db.relationship("Client", back_populates='peers')
    prefixes = db.relationship("Prefix", back_populates='peer')

    def __repr__(self):
        return f'<Peer {self.asn}>'
