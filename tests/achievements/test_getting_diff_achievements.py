from datetime import datetime

import pytest

from rest_framework import status
from rest_framework.test import APIClient
from django.utils.timezone import make_aware
from model_bakery.baker import make

from tests.fixtures import api_client, authenticated_client
from tests.user.fixtures import create_user, user_email, user_password
from tests.counter.urls import get_pull_up_counter_list_url

from user.models import User
from bars.models import Bars
from counter.models import PullUpCounter
from notifications.models import Notification
from achievements.helpers.upsert import upsert_achievements
from achievements.constants import DIFFERENT_BARS_IN_ONE_DAY


def test_getting_achievement_for_3_diff_bars(
    db, authenticated_client: APIClient, user_email
):
    user = User.objects.get(email=user_email)
    upsert_achievements(user, achievements=DIFFERENT_BARS_IN_ONE_DAY)
    bars = make(Bars, 3)
    main_bar = None
    for bar in bars:
        if main_bar is None:
            main_bar = bar
            continue
        counter = make(PullUpCounter, reps=10, bar=bar, user=user)

    achievement_title = None
    for achievement in DIFFERENT_BARS_IN_ONE_DAY:
        if (
            achievement['type'] == 'diff' and
            achievement['threshold'] == 3
        ):
            achievement_title = achievement['title']
            break

    payload = {
        'reps': 5
    }

    assert Notification.objects.count() == 0
    url = get_pull_up_counter_list_url(main_bar.id)
    response = authenticated_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    done_achievement = user.achievements.get(title=achievement_title)
    assert done_achievement.done is True
    assert Notification.objects.count() == 1


@pytest.mark.parametrize(
    'diff_bars,done',
    [
        (2, 0),
        (3, 1),
        (4, 1),
        (5, 2),
        (6, 2),
        (7, 3),
        (8, 3),
        (9, 3),
        (10, 4),
        (11, 4),
    ],
)
def test_getting_lower_achievements_if_higher_achieved(
    db, authenticated_client: APIClient, user_email, diff_bars, done
):
    user = User.objects.get(email=user_email)
    upsert_achievements(user, achievements=DIFFERENT_BARS_IN_ONE_DAY)

    bars = make(Bars, diff_bars)
    main_bar = None
    for bar in bars:
        if main_bar is None:
            main_bar = bar
            continue
        counter = make(PullUpCounter, reps=5, bar=bar, user=user)

    payload = {
        'reps': 10
    }

    url = get_pull_up_counter_list_url(main_bar.id)
    response = authenticated_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    done_achievements = user.achievements.filter(done=True)
    assert done_achievements.count() == done
    assert Notification.objects.count() == done


def test_count_only_reps_from_same_day(
    db, authenticated_client: APIClient, user_email
):
    user = User.objects.get(email=user_email)
    upsert_achievements(user, achievements=DIFFERENT_BARS_IN_ONE_DAY)
    bars = make(Bars, 3)
    main_bar = None
    dates = [
        make_aware(datetime(2023, 9, 11)),
        make_aware(datetime(2023, 9, 12)),
        make_aware(datetime(2023, 9, 13))
    ]
    for bar, date in zip(bars, dates):
        if main_bar is None:
            main_bar = bar
            continue
        counter = make(PullUpCounter, reps=10, bar=bar, user=user)
        counter.created_at = date
        counter.save()

    achievement_title = None
    for achievement in DIFFERENT_BARS_IN_ONE_DAY:
        if (
            achievement['type'] == 'diff' and
            achievement['threshold'] == 3
        ):
            achievement_title = achievement['title']
            break

    payload = {
        'reps': 5
    }

    url = get_pull_up_counter_list_url(main_bar.id)
    response = authenticated_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    done_achievement = user.achievements.get(title=achievement_title)
    assert done_achievement.done is False
