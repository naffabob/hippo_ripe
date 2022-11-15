from flask_restful import abort, Resource
from flask import request
from sqlalchemy.exc import IntegrityError

from webapp.db import db
from webapp.client.models import Client
from webapp.peer.models import Peer


class ClientsApi(Resource):
    def get(self):
        clients = Client.query.all()
        return [{'id': client.id, 'name': client.name} for client in clients]

    def post(self):
        client = Client()
        client.name = request.form['name']
        db.session.add(client)
        try:
            db.session.commit()
        except IntegrityError:
            return {'message': f'Client {client.name} already exist'}
        return {'id': client.id, 'name': client.name}


class ClientApi(Resource):
    def get(self, client_id):
        client = Client.query.get(client_id)
        if not client:
            abort(404, message=f"Client {client_id} doesn't exist")
        return {'id': client.id, 'name': client.name}

    def delete(self, client_id):
        client = Client.query.get(client_id)
        if not client:
            abort(404, message=f"Client {client_id} doesn't exist")

        db.session.delete(client)
        try:
            db.session.commit()
        except IntegrityError:
            return {'message': f'Client {client.name} already exist'}

        return {'message': f'Client {client.name} deleted'}

    def post(self, client_id):
        client = Client.query.get(client_id)
        client.name = request.form['name']
        db.session.add(client)
        try:
            db.session.commit()
        except IntegrityError:
            return {'message': f'Client {client.name} already exist'}

        return {'id': client.id, 'name': client.name}


class PeersApi(Resource):
    def get(self):
        peers = Peer.query.all()
        return [
            {
                'id': peer.id,
                'asn': peer.asn,
                'asset': peer.asset,
                'remark': peer.remark
            } for peer in peers
        ]

    def post(self):
        peer = Peer()
        peer.asn = request.form['asn']
        peer.asset = request.form['asset']
        peer.remark = request.form['remark']
        db.session.add(peer)
        try:
            db.session.commit()
        except IntegrityError:
            return {'message': f'Peer {peer.asn} already exist'}

        return {
            'id': peer.id,
            'asn': peer.asn,
            'asset': peer.asset,
            'remark': peer.remark,
        }


class PeerApi(Resource):
    def get(self):
        pass

    def post(self):
        pass

    def delete(self):
        pass