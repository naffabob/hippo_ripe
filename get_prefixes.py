from webapp import create_app
from webapp.model_db import Peer
from webapp.provider_ripedb import get_prefixes, save_prefixes

app = create_app()
with app.app_context():
    peers = Peer.query.all()
    for peer in peers:
        prefixes = get_prefixes(peer.asn)
        if prefixes:
            save_prefixes(peer=peer.id, prefixes=prefixes)
