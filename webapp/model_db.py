from flask_sqlalchemy import SQLAlchemy

from webapp.settings import PROVIDER_AS

db = SQLAlchemy()


class Provider(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prefix = db.Column(db.String, unique=True, nullable=False)
    description = db.Column(db.String, unique=False, nullable=True)

    def __repr__(self):
        return f'<Provider {PROVIDER_AS} prefixes>'


class Customers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    autnum = db.Column(db.String, unique=True, nullable=False)
    asset = db.Column(db.String, unique=True, nullable=True)
    mntby = db.Column(db.String, unique=False, nullable=False)

    def __repr__(self):
        return f'<{PROVIDER_AS} Customer>'
