import pytest
from django.contrib.gis.geos import Point
from rest_framework import status
from model_bakery.baker import make

from bars.models import Address, Bars
from tests.fixtures import superuser_client, api_client
from tests.user.fixtures import (
    create_superuser, superuser_email, superuser_password
)
from .fixtures import bars_payload, address_payload
from .urls import get_bars_detail_url


def test_update_bars_with_address_success(
        db, superuser_client, bars_payload
):
    address = make(Address)
    bars = make(Bars, address=address)

    assert Address.objects.count() == 1
    assert Bars.objects.count() == 1

    url = get_bars_detail_url(bars.id)
    response = superuser_client.patch(url, bars_payload, format='json')
    assert response.status_code == status.HTTP_200_OK

    address.refresh_from_db()
    bars.refresh_from_db()

    assert bars.title == bars_payload['title']
    assert bars.address == address


def test_update_bars_with_empty_values_fail(db, superuser_client):
    address = make(Address)
    bars = make(Bars, address=address)
    assert Bars.objects.count() == 1

    url = get_bars_detail_url(bars.id)
    payload = {
        'title': '',
        'location': None,
        'address': '',
        'tags': ''
    }
    response = superuser_client.patch(url, payload, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_partial_update_location_only_success(
    db, superuser_client
):
    address = make(Address)
    bars = make(Bars, address=address)

    assert Bars.objects.count() == 1

    url = get_bars_detail_url(bars.id)
    x = 30.234
    y = 20.456
    payload = {
        'location': {
            'type': 'Point',
            'coordinates': [x, y],
        },
    }
    response = superuser_client.patch(url, payload, format='json')
    assert response.status_code == status.HTTP_200_OK

    bars.refresh_from_db()
    assert bars.location.x == x
    assert bars.location.y == y


def test_update_with_coordinates_out_of_range_fail(db, superuser_client):
    address = make(Address)
    bars = make(Bars, address=address, location=Point(0, 0))

    assert Bars.objects.count() == 1

    url = get_bars_detail_url(bars.id)
    x = 300
    y = 200
    payload = {
        'location': {
            'type': 'Point',
            'coordinates': [x, y],
        },
    }
    response = superuser_client.patch(url, payload, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    bars.refresh_from_db()

    assert bars.location.x != x
    assert bars.location.y != y
