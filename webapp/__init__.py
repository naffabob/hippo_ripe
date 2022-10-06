from flask import Flask, render_template, request, redirect, url_for

from webapp.model_db import db, Peer, Prefix
from webapp.forms import PeerForm, PrefixForm


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

    @app.route('/peer/<int:peer_id>', methods=['POST', 'GET'])
    def peer_view(peer_id):
        title = 'Peer settings'
        peer = Peer.query.get(peer_id)
        peer_form = PeerForm(obj=peer)
        if request.method == 'POST':
            peer_form = PeerForm()
            if peer_form.validate_on_submit():
                peer.asn = peer_form.asn.data
                peer.asset = peer_form.asset.data
                peer.client = peer_form.client.data
                db.session.add(peer)
                db.session.commit()
                return redirect(url_for('peer_view', peer_id=peer.id))
        return render_template('peer.html', page_title=title, form=peer_form, peer=peer)

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
