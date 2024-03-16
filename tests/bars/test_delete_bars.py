from rest_framework import status
from model_bakery.baker import make

from bars.models import Bars
from .urls import get_bars_detail_url


def test_delete_success(db, superuser_client):
    bars = make(Bars)

    assert Bars.objects.count() == 1

    url = get_bars_detail_url(bars.id)
    response = superuser_client.delete(url, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Bars.objects.count() == 0


def test_delete_nonexisting_bars_fail(db, superuser_client):
    bars = make(Bars)
    assert Bars.objects.count() == 1

    url = get_bars_detail_url(bars.id + 1)
    response = superuser_client.delete(url, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Bars.objects.count() == 1
