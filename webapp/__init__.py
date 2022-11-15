from flask import Flask, render_template, redirect, url_for
from flask_migrate import Migrate
from flask_restful import Api

from webapp.client.views import blueprint as client_blueprint
from webapp.db import db
from webapp.peer.views import blueprint as peer_blueprint
from webapp.peer.models import Peer
from webapp.prefix.views import blueprint as prefix_blueprint
from webapp.api import ClientApi, ClientsApi, PeerApi, PeersApi


def create_app():
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(ClientsApi, '/api/clients/')
    api.add_resource(ClientApi, '/api/clients/<int:client_id>')
    api.add_resource(PeersApi, '/api/peers/')
    api.add_resource(PeerApi, '/api/peer/<int:peer_id>')

    app.config.from_pyfile('settings.py')
    db.init_app(app)
    migrate = Migrate(app, db)

    app.register_blueprint(client_blueprint)
    app.register_blueprint(peer_blueprint)
    app.register_blueprint(prefix_blueprint)
    app.register_error_handler(404, page_not_found)

    @app.route('/')
    def index():
        return redirect(url_for('peer.peers_view'))

    return app


def page_not_found(e):
    return render_template('404.html'), 404
