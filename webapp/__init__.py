from flask import Flask, render_template

from webapp.client.views import blueprint as client_blueprint
from webapp.db import db
from webapp.peer.views import blueprint as peer_blueprint
from webapp.peer.models import Peer
from webapp.prefix.views import blueprint as prefix_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    db.init_app(app)

    app.register_blueprint(client_blueprint)
    app.register_blueprint(peer_blueprint)
    app.register_blueprint(prefix_blueprint)

    @app.route('/')
    def index():
        title = 'Provider RIPE DB'
        return render_template('index.html', page_title=title)

    return app
