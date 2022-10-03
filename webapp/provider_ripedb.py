import requests

from webapp.model_db import db, Provider, Customers
from webapp.settings import RIPE_ASSET_URL, RIPE_AS_PREFIXES_URL


def get_provider_clients_by_asset() -> dict:
    result = requests.get(RIPE_ASSET_URL)
    clients_data = result.json()
    attribute = clients_data['objects']['object'][0]['attributes']['attribute']
    input_as = {as_['value']: as_['referenced-type'] for as_ in attribute if as_['name'] == 'members'}
    return input_as


def get_maintainers_from_asset(asset: str) -> list:
    api_url = f'https://rest.db.ripe.net/ripe/as-set/{asset}.json'
    result = requests.get(api_url)
    data = result.json()
    attrs = data['objects']['object'][0]['attributes']['attribute']
    mnts_by = [attr['value'] for attr in attrs if 'link' in attr and attr['name'] == 'mnt-by']
    return mnts_by


def get_maintainers_from_autnum(autnum: str) -> list:
    api_url = f'https://rest.db.ripe.net/ripe/aut-num/{autnum}.json'
    result = requests.get(api_url)
    data = result.json()
    if 'objects' not in data:
        return []
    attrs = data['objects']['object'][0]['attributes']['attribute']
    mnts_by = [attr['value'] for attr in attrs if attr['name'] == 'mnt-by']
    mnts_by.remove('RIPE-NCC-END-MNT')
    return mnts_by


def get_autnum_by_maintainers(mnts_by: list) -> list:
    headers = {'Accept': 'application/json'}
    autnums = []
    for mnt in mnts_by:
        api_url = f"http://rest.db.ripe.net/search?inverse-attribute=mnt-by&rflag=true&" \
                  f"query-string={mnt}&source=RIPE&type-filter=aut-num"
        result = requests.get(api_url, headers=headers)
        data = result.json()
        if 'objects' not in data:
            return []
        attrs = data['objects']['object']
        autnums_list = [attr['attributes']['attribute'][0]['value'] for attr in attrs if attr['type'] == 'aut-num']
        autnums.extend(autnums_list)
    return autnums


def get_customers():
    clients = get_provider_clients_by_asset()
    for as_, as_type in clients.items():
        if as_type == 'as-set':
            asset = as_
            maintainers = get_maintainers_from_asset(as_)
            autnum = get_autnum_by_maintainers(maintainers)
            if len(autnum) > 1:
                autnum = ', '.join(autnum)
            elif len(autnum) == 0:
                autnum = ''
            else:
                autnum = autnum[0]
        else:
            autnum = as_
            asset = None
            maintainers = get_maintainers_from_autnum(autnum)

        maintainers_str = ', '.join(maintainers).upper()

        save_customers(autnum=autnum, asset=asset, mntby=maintainers_str)


def save_customers(autnum: str, asset: str, mntby: str):
    customer_exist = Customers.query.filter(Customers.autnum == autnum).count()
    if not customer_exist:
        new_customer = Customers(autnum=autnum, asset=asset, mntby=mntby)
        db.session.add(new_customer)
        db.session.commit()


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
