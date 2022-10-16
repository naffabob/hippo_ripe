from flask import Blueprint, flash, request, render_template, redirect, url_for
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
    ).join(Peer.prefixes, Peer.client).group_by(Peer.id)

    return render_template('peer/peers.html', page=page, peers=peers)


@blueprint.route('/<int:peer_id>', methods=['POST', 'GET'])
def peer_view(peer_id):
    peer = Peer.query.get(peer_id)
    peer_form = PeerForm(obj=peer)
    prefixes = peer.prefixes
    peer_prefixes = {
        'current': [prefix for prefix in prefixes if prefix.state == prefix.STATE_CURRENT],
        'new': [prefix for prefix in prefixes if prefix.state == prefix.STATE_NEW],
        'todelete': [prefix for prefix in prefixes if prefix.state == prefix.STATE_TODELETE]
    }

    if request.method == 'POST':
        peer_form = PeerForm()
        if peer_form.validate_on_submit():
            peer.asn = peer_form.asn.data
            peer.asset = peer_form.asset.data
            peer.remark = peer_form.remark.data
            db.session.add(peer)
            db.session.commit()
            flash('Данные успешно сохранены')
            return redirect(url_for('peer.peers_view'))
    return render_template('peer/peer.html', form=peer_form, peer=peer, peer_prefixes=peer_prefixes)


@blueprint.route('/add', methods=['POST', 'GET'])
def add_peer_view():
    peer = Peer()
    peer_form = PeerForm()
    if request.method == 'POST':
        if peer_form.validate_on_submit():
            peer.asn = peer_form.asn.data
            peer.asset = peer_form.asset.data
            peer.remark = peer_form.remark.data
            db.session.add(peer)
            db.session.commit()
            flash('Данные успешно сохранены')
            return redirect(url_for('peer.peers_view'))
    return render_template('peer/add_peer.html', form=peer_form, peer=peer)
