from flask import Blueprint, flash, request, render_template, redirect, url_for

from webapp.db import db
from webapp.peer.forms import PeerForm
from webapp.peer.models import Peer
from webapp.prefix.models import Prefix

blueprint = Blueprint('peer', __name__, url_prefix='/peers')


@blueprint.route('/')
def peers_view():
    page = 'peers'
    peers = Peer.query.all()
    peer_prefixes = {}
    for peer in peers:
        peer_prefixes[peer.asn] = {
            'current': Prefix.query.filter(Prefix.peer_id == peer.id, Prefix.state == 'current'),
            'new': Prefix.query.filter(Prefix.peer_id == peer.id, Prefix.state == 'new'),
            'todelete': Prefix.query.filter(Prefix.peer_id == peer.id, Prefix.state == 'todelete'),
        }

    return render_template('peer/peers.html', page=page, peers=peers, peer_prefixes=peer_prefixes)


@blueprint.route('/<int:peer_id>', methods=['POST', 'GET'])
def peer_view(peer_id):
    peer = Peer.query.get(peer_id)
    peer_form = PeerForm(obj=peer)
    peer_prefixes = {
        peer.asn:
            {
                'current': Prefix.query.filter(Prefix.peer_id == peer.id, Prefix.state == 'current'),
                'new': Prefix.query.filter(Prefix.peer_id == peer.id, Prefix.state == 'new'),
                'todelete': Prefix.query.filter(Prefix.peer_id == peer.id, Prefix.state == 'todelete')
            }
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
            peer.client_id = peer_form.client.data
            db.session.add(peer)
            db.session.commit()
            flash('Данные успешно сохранены')
            return redirect(url_for('peer.peers_view'))
    return render_template('peer/add_peer.html', form=peer_form, peer=peer)
