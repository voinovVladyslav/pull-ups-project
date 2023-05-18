import pytest
from decimal import Decimal
from rest_framework import status

from bars.models import Address, Bars
from tests.fixtures import api_client
from .fixtures import bars_payload, address_payload
from .urls import BARS_LIST_URL


def test_create_bars_with_address_success(
        db, api_client, bars_payload
):
    assert Address.objects.count() == 0
    assert Bars.objects.count() == 0
    response = api_client.post(BARS_LIST_URL, bars_payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert Address.objects.count() == 1
    assert Bars.objects.count() == 1
    bars = Bars.objects.first()
    address = Address.objects.first()
    assert bars.address == address


def test_create_bars_without_address_fail(db, api_client):
    payload = {
        'title': 'bars title',
        'longitude': Decimal('10.10'),
        'latitude': Decimal('10.10'),
    }
    response = api_client.post(BARS_LIST_URL, payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Bars.objects.count() == 0


def test_create_bars_with_coordinates_out_of_range(
        db, api_client, address_payload
):
    payload = {
        'title': 'bars title',
        'longitude': Decimal('-181.01'),
        'latitude': Decimal('93.00'),
        'address': address_payload
    }
    response = api_client.post(BARS_LIST_URL, payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Bars.objects.count() == 0


def test_create_bars_with_blank_values_fail(db, api_client):
    payload = {
        'title': '',
        'longitude': '',
        'latitude': '',
        'address': {}
    }
    response = api_client.post(BARS_LIST_URL, payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Bars.objects.count() == 0
