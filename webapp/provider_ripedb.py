import requests

from webapp.model_db import db, Provider
from webapp.settings import RIPE_ASSET_URL, RIPE_AS_PREFIXES_URL


def get_provider_clients_by_asset() -> dict:
    result = requests.get(RIPE_ASSET_URL)
    clients_data = result.json()
    attribute = clients_data['objects']['object'][0]['attributes']['attribute']
    input_as = {as_['value']: as_['referenced-type'] for as_ in attribute if as_['name'] == 'members'}
    return input_as


def get_provider_prefixes():
    headers = {'Accept': 'application/json'}
    result = requests.get(RIPE_AS_PREFIXES_URL, headers=headers)
    prefixes_data = result.json()
    if 'objects' not in prefixes_data:
        return False

    objects_values = prefixes_data['objects']['object']
    for object_ in objects_values:
        prefix_value = object_['primary-key']['attribute'][0]
        descr_value = object_['attributes']['attribute'][1]
        if prefix_value['name'] == 'route' and descr_value['name'] == 'descr':
            save_provider_prefixes(prefix=prefix_value['value'], description=descr_value['value'])


def save_provider_prefixes(prefix, description):
    prefix_exist = Provider.query.filter(Provider.prefix == prefix).count()
    if not prefix_exist:
        new_prefix = Provider(prefix=prefix, description=description)
        db.session.add(new_prefix)
        db.session.commit()
