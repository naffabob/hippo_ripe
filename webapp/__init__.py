from flask import Flask
from webapp.provider_ripedb import get_provider_clients_by_asset
from webapp.settings import PROVIDER_ASSET


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        return get_provider_clients_by_asset()

    return app
