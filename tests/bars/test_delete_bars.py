import pytest
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery.baker import make

from bars.models import Address, Bars
from tests.fixtures import api_client
from .fixtures import bars_payload, address_payload, create_bars
from .urls import get_bars_detail_url


def test_delete_success(db, api_client, create_bars):
    bars = create_bars
    assert Bars.objects.count() == 1

    url = get_bars_detail_url(bars.id)
    response = api_client.delete(url, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Bars.objects.count() == 0


def test_delete_nonexisting_bars_fail(db, api_client, create_bars):
    bars = create_bars
    assert Bars.objects.count() == 1

    url = get_bars_detail_url(bars.id + 1)
    response = api_client.delete(url, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Bars.objects.count() == 1
