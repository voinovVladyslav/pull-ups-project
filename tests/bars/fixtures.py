import pytest


@pytest.fixture
def address_payload():
    return {
        'country': 'Ukraine',
        'city': 'Kyiv',
        'street': 'Vasylkivska',
        'number': '34/3',
        'postal_code': '72003',
    }


@pytest.fixture
def bars_payload(address_payload):
    return {
        'title': 'bars title',
        'address': address_payload,
        'location': {
            'type': 'Point',
            'coordinates': [20.34523, 30.234234],
        },
        'tags': {}
    }
