from webapp import create_app
from webapp.provider_ripedb import get_provider_prefixes

app = create_app()
with app.app_context():
    get_provider_prefixes()
