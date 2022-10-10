import requests

from webapp.db import db
from webapp.prefix.models import Prefix


def do_request(url: str) -> dict:
    headers = {'Accept': 'application/json'}
    result = requests.get(url, headers=headers)
    return result.json()


def get_prefixes(asn: str) -> list:
    api_url = f"http://rest.db.ripe.net/search?inverse-attribute=origin&rflag=true&" \
              f"query-string={asn}&source=RIPE&type-filter=route"

    data = do_request(api_url)
    if 'objects' not in data:
        return []

    objects_values = data['objects']['object']

    prefixes = []
    for obj in objects_values:
        prefix_value = obj['primary-key']['attribute'][0]
        if prefix_value['name'] == 'route':
            prefixes.append(prefix_value['value'])
    return prefixes


def save_prefixes(prefixes: list, peer: int):
    for prefix in prefixes:
        prefix_exist = Prefix.query.filter(Prefix.prefix == prefix).count()
        if not prefix_exist:
            db.session.add(Prefix(prefix=prefix, peer_id=peer))
    db.session.commit()
