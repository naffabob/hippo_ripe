from flask import Blueprint, flash, render_template, redirect, url_for, request

from webapp.client.forms import ClientForm
from webapp.client.models import Client
from webapp.db import db

blueprint = Blueprint('client', __name__, url_prefix='/clients')


@blueprint.route('/')
def clients_view():
    clients = Client.query.all()
    page = 'clients'
    return render_template('client/clients.html', clients=clients, page=page)


@blueprint.route('/<int:client_id>', methods=['POST', 'GET'])
def client_view(client_id):
    client = Client.query.get(client_id)
    client_form = ClientForm(obj=client)
    if request.method == 'POST':
        client_form = ClientForm()
        if client_form.validate_on_submit():
            client.name = client_form.name.data
            db.session.add(client)
            db.session.commit()
            flash('Данные успешно сохранены')
            return redirect(url_for('client.clients_view'))
    return render_template('client/client.html', form=client_form, client=client)


@blueprint.route('/add', methods=['POST', 'GET'])
def add_client_view():
    client = Client()
    client_form = ClientForm()
    if request.method == 'POST':
        if client_form.validate_on_submit():
            client.name = client_form.name.data
            db.session.add(client)
            db.session.commit()
            flash('Данные успешно сохранены')
            return redirect(url_for('client.clients_view'))
    return render_template('client/add_client.html', form=client_form, client=client)
