from flask import Flask, render_template, redirect, url_for
from flask_migrate import Migrate

from webapp.client.views import blueprint as client_blueprint
from webapp.db import db
from webapp.peer.views import blueprint as peer_blueprint
from webapp.peer.models import Peer
from webapp.prefix.views import blueprint as prefix_blueprint


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(client_blueprint)
    app.register_blueprint(peer_blueprint)
    app.register_blueprint(prefix_blueprint)
    app.register_error_handler(404, page_not_found)

    @app.route('/')
    def index():
        return redirect(url_for('client.clients_view'))

    return app


def page_not_found(e):
    return render_template('404.html'), 404
