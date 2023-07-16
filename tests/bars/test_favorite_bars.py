import pytest
from rest_framework import status
from model_bakery.baker import make

from bars.models import Address, Bars
from user.models import User
from tests.fixtures import superuser_client, api_client
from tests.user.fixtures import (
    create_superuser, superuser_email, superuser_password
)
from .fixtures import bars_payload, address_payload
from .urls import FAVORITE_BARS, ADD_FAVORITE_BARS, REMOVE_FAVORITE_BARS


def test_list_all_favorite_bars(
    db, superuser_client, superuser_email
):
    bars = make(Bars, 5)
    bar = bars[0]
    user = User.objects.get(email=superuser_email)
    user.favorite_bars.add(bar)

    response = superuser_client.get(FAVORITE_BARS)
    response_data = response.json()['results']
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data) == 1
    assert bar.title in response_data
    assert bars[-1].title not in response_data


def test_list_all_favorite_bars_not_allowed_for_guest_users(
    db, api_client
):
    response = api_client.get(FAVORITE_BARS)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_favorites_have_pagination(db, superuser_client, superuser_email):
    bars = make(Bars, 20)
    user = User.objects.get(email=superuser_email)
    user.favorite_bars.set(bars)
    url = FAVORITE_BARS + '?per_page=10'
    response = superuser_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()
    assert response_data.get('next', None)
    assert len(response_data['results']) == 10


def test_add_bars_to_favorites(db, superuser_client, superuser_email):
    bar = make(Bars)
    user: User = User.objects.get(email=superuser_email)
    assert user.favorite_bars.count() == 0
    payload = {
        'bar_id': bar.id
    }
    response = superuser_client.post(ADD_FAVORITE_BARS, payload)
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.favorite_bars.count() == 1


def test_add_invalid_bars_id_to_favorites(
    db, superuser_client, superuser_email
):
    bar = make(Bars)
    user: User = User.objects.get(email=superuser_email)
    assert user.favorite_bars.count() == 0

    payload = {
        'bar_id': bar.id + 100
    }
    response = superuser_client.post(ADD_FAVORITE_BARS, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    user.refresh_from_db()
    assert user.favorite_bars.count() == 0


def test_remove_bars_from_favorites(db, superuser_client, superuser_email):
    bar = make(Bars)
    user: User = User.objects.get(email=superuser_email)
    user.favorite_bars.add(bar)
    assert user.favorite_bars.count() == 1
    payload = {
        'bar_id': bar.id
    }
    response = superuser_client.post(REMOVE_FAVORITE_BARS, payload)
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.favorite_bars.count() == 0


def test_add_invalid_bars_id_to_favorites(
    db, superuser_client, superuser_email
):
    bar = make(Bars)
    user: User = User.objects.get(email=superuser_email)
    user.favorite_bars.add(bar)
    assert user.favorite_bars.count() == 1
    payload = {
        'bar_id': bar.id + 100
    }
    response = superuser_client.post(REMOVE_FAVORITE_BARS, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    user.refresh_from_db()
    assert user.favorite_bars.count() == 0
