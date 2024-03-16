from datetime import timedelta

from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from model_bakery.baker import make

from user.models import User
from bars.models import Bars
from counter.models import PullUpCounter
from .urls import STATS_URL


def test_stats_fields(db, authenticated_client: APIClient):
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
    make(PullUpCounter, 2, user=user, bar=bar, reps=33)
    response = authenticated_client.get(STATS_URL)

    assert response.status_code == status.HTTP_200_OK
    data = response.json()

    assert data['total_pullups'] == 66
    assert data['max_pullups'] == 33
    assert data['current_streak'] == 1
    assert data['bars_visited'] == 1
    assert data['bars_visited_today'] == 1


def test_no_pullups_means_0_streak(db, authenticated_client: APIClient):
    response = authenticated_client.get(STATS_URL)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['current_streak'] == 0


def test_streak_0_if_no_pullups_yesterday(
    db, authenticated_client: APIClient, user_email
):
    user = User.objects.get(email=user_email)
    bar = make(Bars)
    two_days_ago = timezone.now() - timedelta(days=2)
    counter = make(
        PullUpCounter, user=user, bar=bar, reps=33,
    )
    counter.created_at = two_days_ago
    counter.save()
    response = authenticated_client.get(STATS_URL)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['current_streak'] == 0


def test_streak_1_if_last_pull_up_yesterday(
    db, authenticated_client: APIClient, user_email
):
    user = User.objects.get(email=user_email)
    bar = make(Bars)
    yesterday = timezone.now() - timedelta(days=1)
    counter = make(
        PullUpCounter, user=user, bar=bar, reps=33,
    )
    counter.created_at = yesterday
    counter.save()
    response = authenticated_client.get(STATS_URL)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data['current_streak'] == 1
