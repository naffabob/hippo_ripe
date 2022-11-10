from flask_migrate import upgrade

from webapp import create_app
from webapp.client.models import Client
from webapp.db import db
from webapp.peer.models import Peer

flask_app = create_app()


class TestClient:
    peer = None

    def setup_method(self):
        flask_app.testing = True
        flask_app.config['WTF_CSRF_ENABLED'] = False
        self.peer = flask_app.test_client()
        with flask_app.app_context():
            upgrade()

    def teardown_method(self):
        with flask_app.app_context():
            for table in reversed(db.metadata.sorted_tables):
                db.engine.execute(table.delete())
            db.session.commit()
            db.session.remove()

    def create_client(self, client_name: str) -> Client:
        client = Client()
        client.name = client_name
        db.session.add(client)
        db.session.commit()
        return client

    def create_peer(self, peer_asn: str) -> Peer:
        client = self.create_client('ClientName')
        peer = Peer()
        peer.asn = peer_asn
        peer.client = client
        db.session.add(peer)
        db.session.commit()
        return peer

    def test_peer_view(self):
        with flask_app.app_context():
            peer_asn = 'AS111'
            peer = self.create_peer(peer_asn=peer_asn)

            response = self.peer.get(f'/peers/{peer.id}')
            assert response.status_code == 200
            assert str.encode(peer_asn) in response.data

    def test_create_peer(self):
        with flask_app.app_context():
            peer_asn = 'AS222'
            client = self.create_client('C2')

            form_data = {'asn': peer_asn, 'client': client.id}
            response = self.peer.post('/peers/add', data=form_data)
            assert response.status_code == 302

            peer = Peer.query.filter(Peer.asn == peer_asn).first()
            assert peer
            assert peer.client == client

    def test_update_peer(self):
        with flask_app.app_context():
            peer_asn = 'AS333'
            peer = self.create_peer(peer_asn=peer_asn)

            updated_peer_asn = 'AS333333'
            form_data = {'asn': updated_peer_asn, 'client': peer.client.id}
            response = self.peer.post(f'/peers/{peer.id}', data=form_data)
            assert response.status_code == 302

            updated_peer = Peer.query.get(peer.id)
            assert updated_peer.asn == updated_peer_asn

    def test_peer_exist(self):
        with flask_app.app_context():
            peer_asn = 'AS444'
            peer = self.create_peer(peer_asn=peer_asn)

            form_data = {'asn': peer_asn, 'client': peer.client.id}
            response = self.peer.post('/peers/add', data=form_data)
            assert response.status_code == 302

            peers = Peer.query.all()
            assert len(peers) == 1

    def test_delete_peer(self):
        with flask_app.app_context():
            peer_asn = 'AS555'
            peer = self.create_peer(peer_asn=peer_asn)

            form_data = {'asn': peer_asn, 'client': peer.client.id, 'action': 'delete_peer'}
            response = self.peer.post(f'/peers/{peer.id}', data=form_data)
            assert response.status_code == 302
            assert Peer.query.get(peer.id) is None
