from webapp.db import db


class Client(db.Model):
    __tablename__ = "clients"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    peers = db.relationship("Peer", back_populates='client', cascade='all, delete')

    def __repr__(self):
        return f'<Client {self.name}>'

    def __str__(self):
        return self.name
