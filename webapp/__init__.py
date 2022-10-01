from flask import Flask

from webapp.model_db import db


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    db.init_app(app)

    @app.route('/')
    def index():
        title = 'Provider RIPE DB'
        return render_template('index.html', page_title=title)

    return app
