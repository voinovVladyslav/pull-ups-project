from decimal import Decimal

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
        'longtitude': Decimal('10.10'),
        'latitude': Decimal('10.10'),
        'address': address_payload
    }
