from flask import Flask, render_template

from webapp.model_db import db, Provider, Customers


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    db.init_app(app)

    @app.route('/')
    def index():
        title = 'Provider RIPE DB'
        provider_customers = Customers.query.all()
        provider_prefixes = Provider.query.order_by(Provider.prefix).all()

        return render_template('index.html',
                               page_title=title,
                               prefixes=provider_prefixes,
                               customers=provider_customers,
                               )
    return app
