import os

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


def get_prefixes_bgpq3(ripe_obj) -> set:
    stream = os.popen(f'bgpq3 -J -m 24 {ripe_obj}')
    bgp_output = stream.read()
    prefixes = {line.strip(' ;') for line in bgp_output.splitlines() if '/' in line}
    return prefixes


def save_prefixes(peer_id: int, ripe_prefixes: set):
    db_prefixes = {x.prefix: x for x in Prefix.query.filter(Prefix.peer_id == peer_id)}

    ripe_new = ripe_prefixes - db_prefixes.keys()

    for prefix_obj in db_prefixes.values():
        if prefix_obj.prefix in ripe_prefixes:
            if prefix_obj.state == Prefix.STATE_TODELETE:
                prefix_obj.state = Prefix.STATE_CURRENT
                db.session.add(prefix_obj)
        else:
            prefix_obj.state = Prefix.STATE_TODELETE
            db.session.add(prefix_obj)

    for prefix in ripe_new:
        prefix_obj = Prefix(prefix=prefix, state=Prefix.STATE_NEW, peer_id=peer_id)
        db.session.add(prefix_obj)

    db.session.commit()
