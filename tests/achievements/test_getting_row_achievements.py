from datetime import timedelta

import pytest

from rest_framework import status
from rest_framework.test import APIClient
from django.utils import timezone
from model_bakery.baker import make

from tests.fixtures import api_client, authenticated_client
from tests.user.fixtures import create_user, user_email, user_password
from tests.counter.urls import get_pull_up_counter_list_url

from user.models import User
from bars.models import Bars
from counter.models import PullUpCounter
from achievements.helpers.upsert import upsert_achievements
from achievements.constants import PULL_UP_DAY_STREAK_ACHIEVEMENTS


def test_getting_achievement_for_7_day_stread(
    db, authenticated_client: APIClient, user_email
):
    user = User.objects.get(email=user_email)
    upsert_achievements(
        user, achievements=PULL_UP_DAY_STREAK_ACHIEVEMENTS
    )
    bar = make(Bars)
    number_of_days = 6
    now = timezone.now()
    starting_point = now - timedelta(days=number_of_days)

    for _ in range(number_of_days):
        counter = make(PullUpCounter, bar=bar, user=user, reps=10)
        counter.created_at = starting_point
        counter.save()
        starting_point = starting_point + timedelta(days=1)

    achievement_title = None
    for achievement in PULL_UP_DAY_STREAK_ACHIEVEMENTS:
        if (
            achievement['type'] == 'row' and
            achievement['threshold'] == 7
        ):
            achievement_title = achievement['title']
            break

    payload = {
        'reps': 10
    }

    url = get_pull_up_counter_list_url(bar.id)
    response = authenticated_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    done_achievement = user.achievements.get(title=achievement_title)
    assert done_achievement.done is True


@pytest.mark.parametrize(
    'streak,done',
    [
        (5, 0),
        (7, 1),
        (10, 1),
        (16, 2),
        (25, 2),
        (30, 3),
        (35, 3),
    ],
)
def test_getting_lower_achievements_if_higher_achieved(
    db, authenticated_client: APIClient, user_email, streak, done
):
    user = User.objects.get(email=user_email)
    upsert_achievements(
        user, achievements=PULL_UP_DAY_STREAK_ACHIEVEMENTS
    )
    bar = make(Bars)
    now = timezone.now()
    starting_point = now - timedelta(days=streak - 1)

    for _ in range(streak - 1):
        counter = make(PullUpCounter, bar=bar, user=user, reps=10)
        counter.created_at = starting_point
        counter.save()
        starting_point = starting_point + timedelta(days=1)

    payload = {
        'reps': 10
    }

    url = get_pull_up_counter_list_url(bar.id)
    response = authenticated_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    done_achievements = user.achievements.filter(done=True)
    assert done_achievements.count() == done


def test_0_reps_does_not_included(
    db, authenticated_client: APIClient, user_email
):
    user = User.objects.get(email=user_email)
    upsert_achievements(
        user, achievements=PULL_UP_DAY_STREAK_ACHIEVEMENTS
    )
    bar = make(Bars)
    number_of_days = 6
    now = timezone.now()
    starting_point = now - timedelta(days=number_of_days)

    for _ in range(number_of_days):
        counter = make(PullUpCounter, bar=bar, user=user, reps=0)
        counter.created_at = starting_point
        counter.save()
        starting_point = starting_point + timedelta(days=1)

    achievement_title = None
    for achievement in PULL_UP_DAY_STREAK_ACHIEVEMENTS:
        if (
            achievement['type'] == 'row' and
            achievement['threshold'] == 7
        ):
            achievement_title = achievement['title']
            break

    payload = {
        'reps': 10
    }

    url = get_pull_up_counter_list_url(bar.id)
    response = authenticated_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    done_achievement = user.achievements.get(title=achievement_title)
    assert done_achievement.done is False
