from decimal import Decimal

import pytest

from bars.models import Address, Bars


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
        'longitude': Decimal('10.10'),
        'latitude': Decimal('10.10'),
        'address': address_payload
    }


@pytest.fixture
def create_bars(db, address_payload, bars_payload):
    address = Address.objects.create(**address_payload)
    bars_payload['address'] = address
    bars = Bars.objects.create(**bars_payload)
    return bars
