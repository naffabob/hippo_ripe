from flask import Flask, render_template

from webapp.provider_ripedb import get_provider_clients_by_asset
from webapp.settings import PROVIDER_ASSET


def create_app():
    app = Flask(__name__)

    @app.route('/')
    def index():
        title = 'Provider RIPE DB'
        return render_template('index.html', page_title=title)

    return app
