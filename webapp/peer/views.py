from datetime import date

from flask import abort, Blueprint, flash, request, render_template, redirect, url_for, Response
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import case

from webapp.client.models import Client
from webapp.db import db
from webapp.peer.forms import PeerForm
from webapp.peer.models import Peer
from webapp.prefix.models import Prefix

blueprint = Blueprint('peer', __name__, url_prefix='/peers')


@blueprint.route('/')
def peers_view():
    page = 'peers'
    peers = db.session.query(
        Peer.id,
        Peer.asn,
        Peer.asset,
        Client.name,
        Peer.remark,
        func.count(
            case(
                [(Prefix.state == Prefix.STATE_CURRENT, 1)],
                else_=None
            )
        ).label(Prefix.STATE_CURRENT),
        func.count(
            case(
                [(Prefix.state == Prefix.STATE_NEW, 1)],
                else_=None
            )
        ).label(Prefix.STATE_NEW),
        func.count(
            case(
                [(Prefix.state == Prefix.STATE_TODELETE, 1)],
                else_=None
            )
        ).label(Prefix.STATE_TODELETE),
    ).join(Peer.prefixes, Peer.client, isouter=True).group_by(Peer.id)

    return render_template('peer/peers.html', page=page, peers=peers)


@blueprint.route('/<int:peer_id>', methods=['POST', 'GET'])
def peer_view(peer_id):
    peer = Peer.query.get(peer_id)
    if not peer:
        abort(404)

    peer_form = PeerForm(obj=peer)
    clients = Client.query.all()
    choices = [(0, '----')] + [(c.id, c.name) for c in clients]  # BAD zero first value
    peer_form.client.choices = choices
    peer_form.client.data = peer.client.id

    prefixes = peer.prefixes
    peer_prefixes = {
        'current': [prefix for prefix in prefixes if prefix.state == prefix.STATE_CURRENT],
        'new': [prefix for prefix in prefixes if prefix.state == prefix.STATE_NEW],
        'todelete': [prefix for prefix in prefixes if prefix.state == prefix.STATE_TODELETE]
    }

    if request.method == 'POST':
        action = request.form.get("action", None)
        if action == 'delete_peer':
            db.session.delete(peer)
            db.session.commit()
            flash('Peer deleted', category='success')
            return redirect(url_for('peer.peers_view'))

        peer_form = PeerForm()
        peer_form.client.choices = choices
        if peer_form.validate_on_submit():
            peer.asn = peer_form.asn.data
            peer.asset = peer_form.asset.data
            peer.client_id = peer_form.client.data
            peer.remark = peer_form.remark.data
            db.session.add(peer)
            try:
                db.session.commit()
            except IntegrityError:
                flash('Такой клиент уже существует', category='error')
                return redirect(url_for('peer.peer_view', peer_id=peer_id))

            flash('Данные успешно сохранены', category='success')
            return redirect(url_for('peer.peers_view'))
    return render_template('peer/peer.html', form=peer_form, peer=peer, peer_prefixes=peer_prefixes)


@blueprint.route('/add', methods=['POST', 'GET'])
def add_peer_view():
    peer = Peer()

    peer_form = PeerForm()
    clients = Client.query.all()
    choices = [(0, '----')] + [(c.id, c.name) for c in clients]  # BAD zero first value
    peer_form.client.choices = choices

    if request.method == 'POST':
        if peer_form.validate_on_submit():
            peer.asn = peer_form.asn.data
            peer.asset = peer_form.asset.data
            peer.remark = peer_form.remark.data
            peer.client_id = peer_form.client.data
            db.session.add(peer)
            try:
                db.session.commit()
            except IntegrityError:
                flash('Такой клиент уже существует', category='error')
                return redirect(url_for('peer.add_peer_view'))

            flash('Данные успешно сохранены', category='success')
            return redirect(url_for('peer.peers_view'))

    return render_template('peer/add_peer.html', form=peer_form, peer=peer)


@blueprint.route('/<int:peer_id>/config')
def peer_config_view(peer_id):
    peer = Peer.query.get(peer_id)
    if not peer:
        abort(404)

    today_date = date.today().strftime('%Y-%m-%d')

    return render_template('peer/config.html', peer=peer, date=today_date)


@blueprint.route('/<int:peer_id>/config_plain')
def peer_plain_config_view(peer_id):
    peer = Peer.query.get(peer_id)
    if not peer:
        abort(404)

    today_date = date.today().strftime('%Y-%m-%d')

    output = render_template('peer/config.txt', peer=peer, date=today_date)

    return Response(output, mimetype='text/plain')
