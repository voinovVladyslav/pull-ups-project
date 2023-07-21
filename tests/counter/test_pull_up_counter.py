import json

import pytest
from rest_framework import status
from model_bakery.baker import make

from counter.models import PullUpCounter
from bars.models import Bars
from user.models import User
from tests.fixtures import superuser_client, api_client
from tests.user.fixtures import (
    create_superuser, superuser_email, superuser_password,
    user_email, user_password, create_user,
)
from .urls import get_pull_up_counter_detail_url, get_pull_up_counter_list_url


def test_authentication_required(
    db, api_client, superuser_client, superuser_email
):
    bar = make(Bars)
    user = User.objects.get(email=superuser_email)
    count = make(PullUpCounter, bar=bar, user=user)

    url = get_pull_up_counter_list_url(bar.id)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    response = superuser_client.get(url)
    assert response.status_code == status.HTTP_200_OK


def test_return_only_user_related_counter(
    db, superuser_client, superuser_email, create_user
):
    bar = make(Bars)
    user = User.objects.get(email=superuser_email)
    second_user = create_user()
    counters = make(PullUpCounter, 5, user=user)
    second_user_counters = make(PullUpCounter, 5, user=second_user)

    url = get_pull_up_counter_list_url(bar.id)
    response = superuser_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_data = json.loads(response.data)
    response_counters = response_data['results']
    assert len(response_counters) == 5

    for c in response_counters:
        assert c['user'] == user.id


def test_create_counter(db, superuser_client, superuser_email):
    bar = make(Bars)
    user = User.objects.get(email=superuser_email)
    payload = {
        'reps': 10,
    }
    assert PullUpCounter.objects.count() == 0
    url = get_pull_up_counter_list_url(bar.id)
    response = superuser_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert PullUpCounter.objects.count() == 1
    counter = PullUpCounter.objects.first()
    assert counter.reps == payload['reps']
    assert counter.user == user
    assert counter.bar == bar


def test_create_counter_invalid_bars_id(db, superuser_client):
    bar = make(Bars)
    payload = {
        'reps': 10,
    }
    assert PullUpCounter.objects.count() == 0
    url = get_pull_up_counter_list_url(bar.id + 1)
    response = superuser_client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert PullUpCounter.objects.count() == 0


def test_update_counter(db, superuser_client, superuser_email):
    bar = make(Bars)
    user = User.objects.get(email=superuser_email)
    counter = make(PullUpCounter, user=user, bar=bar, reps=10)
    payload = {
        'reps': 20
    }
    url = get_pull_up_counter_detail_url(bar.id, counter.id)
    response = superuser_client.patch(url, payload)
    assert response.status_code == status.HTTP_200_OK
    counter.refresh_from_db()
    assert counter.reps == payload['reps']


def test_update_counter_invalid_payload(db, superuser_client, superuser_email):
    bar = make(Bars)
    user = User.objects.get(email=superuser_email)
    reps = 10
    counter = make(PullUpCounter, user=user, bar=bar, reps=reps)
    payload = {
        'reps': 'hello'
    }
    url = get_pull_up_counter_detail_url(bar.id, counter.id)
    response = superuser_client.patch(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    counter.refresh_from_db()
    assert counter.reps == reps


def test_delete_counter(db, superuser_client, superuser_email):
    bar = make(Bars)
    user = User.objects.get(email=superuser_email)
    counter = make(PullUpCounter, user=user, bar=bar)
    assert PullUpCounter.objects.count() == 1

    url = get_pull_up_counter_detail_url(bar.id, counter.id)
    response = superuser_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert PullUpCounter.objects.count() == 0


def test_delete_counter_invalid_id(db, superuser_client, superuser_email):
    bar = make(Bars)
    user = User.objects.get(email=superuser_email)
    counter = make(PullUpCounter, user=user, bar=bar)
    assert PullUpCounter.objects.count() == 1

    url = get_pull_up_counter_detail_url(bar.id, counter.id + 1)
    response = superuser_client.delete(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert PullUpCounter.objects.count() == 1


def test_delete_counter_using_different_bars_id_result_in_error(
    db, superuser_client, superuser_email,
):
    bar, bar2 = make(Bars, 2)
    user = User.objects.get(email=superuser_email)
    counter = make(PullUpCounter, user=user, bar=bar)
    assert PullUpCounter.objects.count() == 1

    url = get_pull_up_counter_detail_url(bar2.id, counter.id)
    response = superuser_client.delete(url)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert PullUpCounter.objects.count() == 1
