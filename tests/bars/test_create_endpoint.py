import pytest
from rest_framework import status

from bars.models import Address, Bars
from tests.fixtures import api_client, superuser_client
from .fixtures import bars_payload, address_payload
from tests.user.fixtures import (
    create_superuser, superuser_email, superuser_password
)
from .urls import BARS_LIST_URL


@pytest.mark.xfail
def test_create_bars_with_address_success(
        db, superuser_client, bars_payload
):
    assert Address.objects.count() == 0
    assert Bars.objects.count() == 0
    response = superuser_client.post(
        BARS_LIST_URL, bars_payload, format='json'
    )
    assert response.status_code == status.HTTP_201_CREATED
    assert Address.objects.count() == 1
    assert Bars.objects.count() == 1
    bars = Bars.objects.first()
    address = Address.objects.first()
    assert bars.address == address
    assert bars.location is not None


def test_create_bars_without_address_fail(db, superuser_client):
    payload = {
        'title': 'bars title',
    }
    response = superuser_client.post(BARS_LIST_URL, payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Bars.objects.count() == 0


def test_create_bars_with_coordinates_out_of_range(
        db, superuser_client, address_payload
):
    payload = {
        'title': 'bars title',
        'locations': {
            'coordinates': [200, 300],
        },
        'address': address_payload
    }
    response = superuser_client.post(BARS_LIST_URL, payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Bars.objects.count() == 0


def test_create_bars_with_blank_values_fail(db, superuser_client):
    payload = {
        'title': '',
        'locations': {
            'coordinates': [],
        },
        'address': {}
    }
    response = superuser_client.post(BARS_LIST_URL, payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Bars.objects.count() == 0
