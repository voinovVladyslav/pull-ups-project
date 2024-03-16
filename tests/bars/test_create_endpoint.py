from rest_framework import status

from pullupbars.models import PullUpBars
from .urls import BARS_LIST_URL


def test_create_bars_with_coordinates_out_of_range(db, superuser_client):
    payload = {
        'title': 'bars title',
        'locations': {
            'coordinates': [200, 300],
        },
    }
    response = superuser_client.post(BARS_LIST_URL, payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert PullUpBars.objects.count() == 0


def test_create_bars_with_blank_values_fail(db, superuser_client):
    payload = {
        'title': '',
        'locations': {
            'coordinates': [],
        },
    }
    response = superuser_client.post(BARS_LIST_URL, payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert PullUpBars.objects.count() == 0
