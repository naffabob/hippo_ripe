from flask import Blueprint, flash, render_template, redirect, url_for, request
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql import func

from webapp.client.forms import ClientForm
from webapp.client.models import Client
from webapp.db import db

blueprint = Blueprint('client', __name__, url_prefix='/clients')


@blueprint.route('/')
def clients():
    all_clients = db.session.query(
        Client.id,
        Client.name,
        func.count(Client.peers).label('total_peers'),
    ).join(Client.peers, isouter=True).group_by(Client.name)

    page = 'clients'
    return render_template('client/clients.html', clients=all_clients, page=page)


@blueprint.route('/<int:client_id>', methods=['POST', 'GET'])
def client(client_id):
    client = Client.query.get(client_id)
    client_form = ClientForm(obj=client)
    if request.method == 'POST':
        client_form = ClientForm()
        if client_form.validate_on_submit():
            client.name = client_form.name.data
            db.session.add(client)
            try:
                db.session.commit()
            except IntegrityError:
                flash('Такой клиент уже существует', category='error')
                return redirect(url_for('client.client', client_id=client_id))

            flash('Данные успешно сохранены', category='success')
            return redirect(url_for('client.clients'))

    return render_template('client/client.html', form=client_form, client=client)


@blueprint.route('/add', methods=['POST', 'GET'])
def add_client():
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
                return redirect(url_for('client.add_client'))

            flash('Данные успешно сохранены', category='success')
            return redirect(url_for('client.clients'))
    return render_template('client/add_client.html', form=client_form, client=client)
