from flask import abort, Blueprint, flash, render_template, redirect, url_for, request

from webapp.client.forms import ClientForm
from webapp.client.models import Client
from webapp.db import db

blueprint = Blueprint('client', __name__, url_prefix='/clients')


@blueprint.route('/')
def clients():
    clients = Client.query.all()
    page = 'clients'
    return render_template('client/clients.html', clients=clients, page=page)


@blueprint.route('/<int:client_id>', methods=['POST', 'GET'])
def client(client_id):
    client = Client.query.get(client_id)
    if not client:
        abort(404)

    client_form = ClientForm(obj=client)
    if request.method == 'POST':
        action = request.form.get("action", None)
        if action == 'delete_client':
            db.session.delete(client)
            db.session.commit()
            flash('Client deleted', category='success')
            return redirect(url_for('client.clients'))

        client_form = ClientForm()
        if client_form.validate_on_submit():
            client.name = client_form.name.data
            db.session.add(client)
            db.session.commit()
            flash('Данные успешно сохранены')
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
            db.session.commit()
            flash('Данные успешно сохранены')
            return redirect(url_for('client.clients'))
    return render_template('client/add_client.html', form=client_form, client=client)
