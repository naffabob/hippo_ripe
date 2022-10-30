from flask import abort, Blueprint, flash, render_template, redirect, url_for, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func

from webapp.client.forms import ClientForm, ClentPeerForm
from webapp.client.models import Client
from webapp.db import db
from webapp.peer.models import Peer

blueprint = Blueprint('client', __name__, url_prefix='/clients')


@blueprint.route('/')
def clients_view():
    page = 'clients'

    clients = db.session.query(
        Client.id,
        Client.name,
        func.count(Peer.id)
    ).join(Client.peers, isouter=True).group_by(Client.id)

    search_str = request.args.get('search')
    if search_str:
        search = f'%{search_str}%'
        clients = clients.filter(Client.name.like(search))

    return render_template('client/clients.html', clients=clients, page=page, search_str=search_str)


@blueprint.route('/<int:client_id>', methods=['POST', 'GET'])
def client_view(client_id):
    client = Client.query.get(client_id)
    if not client:
        abort(404)

    client_form = ClientForm(obj=client)
    peer_form = ClentPeerForm()

    if request.method == 'POST':
        action = request.form.get("action", None)
        back = url_for('client.client_view', client_id=client_id)

        if action == 'delete_client':
            db.session.delete(client)
            db.session.commit()
            flash('Client deleted', category='success')
            return redirect(url_for('client.clients_view'))

        if action == 'update_client':
            if client_form.validate_on_submit():
                client.name = client_form.name.data
                db.session.add(client)
                try:
                    db.session.commit()
                except IntegrityError:
                    flash('Такой клиент уже существует', category='error')
                    return redirect(back)

                flash('Данные успешно сохранены', category='success')
                return redirect(back)

        if action == 'create_peer':
            if peer_form.validate_on_submit():
                peer = Peer()
                peer.asn = peer_form.asn.data
                peer.asset = peer_form.asset.data
                peer.remark = peer_form.remark.data
                peer.client_id = client.id
                db.session.add(peer)
                try:
                    db.session.commit()
                except IntegrityError:
                    flash('Такой peer уже существует', category='error')
                    return redirect(back)

                flash('Данные успешно сохранены', category='success')
                return redirect(back)

    return render_template('client/client.html', form=client_form, client=client, peer_form=peer_form)


@blueprint.route('/add', methods=['POST', 'GET'])
def add_client_view():
    client = Client()
    client_form = ClientForm()
    if request.method == 'POST':
        if client_form.validate_on_submit():
            client.name = client_form.name.data
            db.session.add(client)
            try:
                db.session.commit()
            except IntegrityError:
                flash(f'Такой клиент уже существует', category='error')
                return redirect(url_for('client.add_client_view'))

            flash('Данные успешно сохранены', category='success')
            return redirect(url_for('client.client_view', client_id=client.id))
    return render_template('client/add_client.html', form=client_form, client=client)
