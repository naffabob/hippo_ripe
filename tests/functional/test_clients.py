from flask_migrate import upgrade

from webapp import create_app
from webapp.client.models import Client
from webapp.db import db

flask_app = create_app()


class TestClient:
    client = None

    def setup_method(self):
        flask_app.testing = True
        flask_app.config['WTF_CSRF_ENABLED'] = False
        self.client = flask_app.test_client()
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

    def test_client_view(self):
        with flask_app.app_context():
            client_name = 'C1'
            client = self.create_client(client_name)

            response = self.client.get(f'/clients/{client.id}')
            assert response.status_code == 200
            assert str.encode(client_name) in response.data

    def test_create_client(self):
        with flask_app.app_context():
            client_name = 'C2'

            form_data = {'name': client_name}
            response = self.client.post('/clients/add', data=form_data)
            assert response.status_code == 302

            client = Client.query.filter(Client.name == client_name).first()
            assert client

    def test_update_client(self):
        with flask_app.app_context():
            client = self.create_client('C3')
            updated_client_name = 'C4'

            form_data = {'name': updated_client_name, 'action': 'update_client'}
            response = self.client.post(f'/clients/{client.id}', data=form_data)
            assert response.status_code == 302

            updated_client = Client.query.get(client.id)
            assert updated_client.name == updated_client_name

    def test_client_exist(self):
        with flask_app.app_context():
            client_name = 'C6'
            self.create_client(client_name)

            form_data = {'name': client_name}
            response = self.client.post('/clients/add', data=form_data)
            assert response.status_code == 302

            clients = Client.query.all()
            assert len(clients) == 1

    def test_delete_client(self):
        with flask_app.app_context():
            client_name = 'C7'
            client = self.create_client(client_name)

            form_data = {'name': client_name, 'action': 'delete_client'}
            response = self.client.post(f'/clients/{client.id}', data=form_data)
            assert response.status_code == 302
            assert Client.query.get(client.id) is None
