import pytest
from decimal import Decimal
from rest_framework import status
from model_bakery.baker import make

from bars.models import Address, Bars
from tests.fixtures import api_client
from .fixtures import bars_payload, address_payload, create_bars
from .urls import get_bars_detail_url


def test_update_bars_with_address_success(
        db, api_client, bars_payload
):
    address = make(Address)
    bars = make(Bars, address=address)

    assert Address.objects.count() == 1
    assert Bars.objects.count() == 1

    url = get_bars_detail_url(bars.id)
    response = api_client.patch(url, bars_payload, format='json')
    assert response.status_code == status.HTTP_200_OK

    address.refresh_from_db()
    bars.refresh_from_db()

    assert bars.title == bars_payload['title']
    assert bars.latitude == bars_payload['latitude']
    assert bars.longitude == bars_payload['longitude']
    assert bars.address == address


def test_update_bars_with_empty_values_fail(db, api_client, create_bars):
    bars = create_bars

    assert Bars.objects.count() == 1

    url = get_bars_detail_url(bars.id)
    payload = {
        'title': '',
        'longitude': '',
        'latitude': '',
        'address': ''
    }
    response = api_client.patch(url, payload, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.xfail
def test_partial_update_address_only_success(db, api_client, create_bars):
    assert False


@pytest.mark.parametrize(
    'object_name, value',
    [
        ('title', 'Updated Country', ),
        ('longitude', Decimal('110.00')),
        ('latitude', Decimal('60.00')),
    ],
    ids=[
        'title UPDATE',
        'longitude UPDATE',
        'latitude UPDATE',
    ]
)
def test_partial_update_bars_only_success(
    db, api_client, create_bars, object_name, value
):
    bars = create_bars

    assert Bars.objects.count() == 1

    url = get_bars_detail_url(bars.id)
    payload = {
        object_name: value
    }
    response = api_client.patch(url, payload, format='json')

    assert response.status_code == status.HTTP_200_OK

    bars.refresh_from_db()

    assert getattr(bars, object_name) == payload[object_name]


def test_update_with_coordinates_out_of_range_fail(db, api_client, create_bars):
    bars = create_bars

    assert Bars.objects.count() == 1

    url = get_bars_detail_url(bars.id)
    payload = {
        'longitude': Decimal('-190.00'),
        'latitude': Decimal('95.00'),
    }
    response = api_client.patch(url, payload, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST

    bars.refresh_from_db()

    assert bars.longitude != payload['longitude']
    assert bars.latitude != payload['latitude']
