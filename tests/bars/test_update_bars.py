from django.contrib.gis.geos import Point
from rest_framework import status
from model_bakery.baker import make

from bars.models import Bars
from .urls import get_bars_detail_url



def test_update_bars_with_empty_values_fail(db, superuser_client):
    bars = make(Bars)
    assert Bars.objects.count() == 1

    url = get_bars_detail_url(bars.id)
    payload = {
        'title': '',
        'location': None,
        'tags': ''
    }
    response = superuser_client.patch(url, payload, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_partial_update_location_only_success(
    db, superuser_client
):
    bars = make(Bars)

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
    bars = make(Bars, location=Point(0, 0))

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
