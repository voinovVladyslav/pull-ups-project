import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from model_bakery.baker import make

from user.models import User
from bars.models import Bars
from counter.models import PullUpCounter
from tests.fixtures import api_client, authenticated_client
from .fixtures import user_email, user_password, create_user
from .urls import STATS_URL


def test_stats_fields(db, authenticated_client: APIClient, user_email):
    response = authenticated_client.get(STATS_URL)
    assert response.status_code == status.HTTP_200_OK
    fields = [
        'current_streak',
        'total_pullups',
        'max_pullups',
        'bars_visited',
        'bars_visited_today',
    ]
    for field in fields:
        assert field in response.json()
        assert response.json()[field] == 0


def test_calculated_stats(db, authenticated_client: APIClient, user_email):
    user = User.objects.get(email=user_email)
    bar = make(Bars)
    counter = make(PullUpCounter, 2, user=user, bar=bar, reps=33)
    response = authenticated_client.get(STATS_URL)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data['total_pullups'] == 66
    assert data['max_pullups'] == 33
    assert data['current_streak'] == 1
    assert data['bars_visited'] == 1
    assert data['bars_visited_today'] == 1
