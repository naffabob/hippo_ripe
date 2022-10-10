from flask import Blueprint, request, render_template, redirect, url_for

from webapp.model_db import db
from webapp.peer.forms import PeerForm
from webapp.peer.models import Peer
from webapp.client.models import Client

blueprint = Blueprint('peer', __name__, url_prefix='/peers')


@blueprint.route('/')
def peers_view():
    peers = Peer.query.all()
    page = 'peers'
    return render_template('peer/peers.html', peers=peers, page=page)


@blueprint.route('/<int:peer_id>', methods=['POST', 'GET'])
def peer_view(peer_id):
    peer = Peer.query.get(peer_id)
    peer_form = PeerForm(obj=peer)
    if request.method == 'POST':
        peer_form = PeerForm()
        if peer_form.validate_on_submit():
            peer.asn = peer_form.asn.data
            peer.asset = peer_form.asset.data
            peer.remark = peer_form.remark.data
            db.session.add(peer)
            db.session.commit()
            return redirect(url_for('peer.peers_view'))
    return render_template('peer/peer.html', form=peer_form, peer=peer)


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
            return redirect(url_for('peer.peers_view'))
    return render_template('peer/add_peer.html', form=peer_form, peer=peer)
