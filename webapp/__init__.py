from flask import Flask, render_template

from webapp.model_db import db, Peer, Prefix


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    db.init_app(app)

    @app.route('/')
    def index():
        title = 'Provider RIPE DB'
        provider_customers = Peer.query.all()
        return render_template('index.html',
                               page_title=title,
                               customers=provider_customers,
                               )
    return app
