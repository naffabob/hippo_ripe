from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Prefix(db.Model):
    __tablename__ = "prefixes"
    id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.String, unique=False, nullable=False)
    peer_id = db.Column(db.Integer, db.ForeignKey("peers.id", ondelete="CASCADE"), nullable=False)
    peer = db.relationship("Peer", back_populates='prefixes')

    def __repr__(self):
        return f'<Prefix {self.prefix}>'

    def __str__(self):
        return self.prefix
