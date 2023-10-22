import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from tests.fixtures import api_client, authenticated_client
from .fixtures import user_email, user_password, create_user
from .urls import STATS_URL


def test_stats_fields(db, authenticated_client: APIClient, user_email):
    response = authenticated_client.get(STATS_URL)
    assert response.status_code == status.HTTP_200_OK
    fields = [
        'total_pullups',
        'max_pullups',
        'total_bars_visited',
        'current_streak',
    ]
    for field in fields:
        assert field in response.json()
