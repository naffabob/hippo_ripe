from webapp import create_app
from webapp.provider_ripedb import get_customers

app = create_app()
with app.app_context():
    get_customers()
