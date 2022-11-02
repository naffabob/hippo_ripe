from webapp import create_app
from webapp.peer.models import Peer
from webapp.provider_ripedb import save_prefixes, update_prefixes_bgpq3

app = create_app()
with app.app_context():
    peers = Peer.query.all()
    for peer in peers:
        prefixes = update_prefixes_bgpq3(peer.asset or peer.asn)
        if prefixes:
            save_prefixes(peer_id=peer.id, ripe_prefixes=prefixes)
