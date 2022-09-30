import requests
from pprint import pprint

from webapp.settings import RIPE_ASSET_URL


def get_provider_clients_by_asset() -> dict:
    result = requests.get(RIPE_ASSET_URL)
    clients_data = result.json()
    attribute = clients_data['objects']['object'][0]['attributes']['attribute']
    input_as = {as_['value']: as_['referenced-type'] for as_ in attribute if as_['name'] == 'members'}
    return input_as


if __name__ == "__main__":
    pprint(get_provider_clients_by_asset())
