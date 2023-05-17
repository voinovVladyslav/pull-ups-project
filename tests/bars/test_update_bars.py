import pytest
from rest_framework import status
from model_bakery.baker import make

from bars.models import Address, Bars
from tests.fixtures import api_client
from .fixtures import bars_payload, address_payload
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
