from flask import Flask, render_template, request, redirect, url_for

from webapp.client.views import blueprint as client_blueprint
from webapp.forms import PrefixForm
from webapp.model_db import db, Prefix
from webapp.peer.views import blueprint as peer_blueprint
from webapp.peer.models import Peer


def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('settings.py')
    db.init_app(app)

    app.register_blueprint(client_blueprint)
    app.register_blueprint(peer_blueprint)

    @app.route('/')
    def index():
        title = 'Provider RIPE DB'
        clients = Peer.query.all()
        return render_template('index.html', page_title=title, customers=clients)

    @app.route('/prefixes/<int:prefix_id>', methods=['POST', 'GET'])
    def prefix_view(prefix_id):
        prefix = Prefix.query.get(prefix_id)
        prefix_form = PrefixForm(obj=prefix)
        if request.method == 'POST':
            prefix_form = PrefixForm()
            if prefix_form.validate_on_submit():
                prefix.prefix = prefix_form.prefix.data
                db.session.add(prefix)
                db.session.commit()
                return redirect(url_for('prefix_view', prefix_id=prefix.id))

        return render_template('prefix.html', form=prefix_form, prefix=prefix)

    return app
