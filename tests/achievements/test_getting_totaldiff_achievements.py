import pytest

from rest_framework import status
from rest_framework.test import APIClient
from model_bakery.baker import make

from tests.counter.urls import get_pull_up_counter_list_url

from user.models import User
from bars.models import Bars
from counter.models import PullUpCounter
from notifications.models import Notification
from achievements.helpers.upsert import upsert_achievements
from achievements.constants import TOTAL_DIFFERENT_PULL_UP_BARS_ACHIEVEMENTS


def test_getting_achievement_for_5_different_bars(
    db, authenticated_client: APIClient, user_email
):
    user = User.objects.get(email=user_email)
    upsert_achievements(
        user, achievements=TOTAL_DIFFERENT_PULL_UP_BARS_ACHIEVEMENTS
    )
    bars = make(Bars, 5)
    main_bar = None
    for bar in bars:
        if main_bar is None:
            main_bar = bar
            continue
        make(PullUpCounter, reps=10, bar=bar, user=user)

    achievement_title = None
    for achievement in TOTAL_DIFFERENT_PULL_UP_BARS_ACHIEVEMENTS:
        if (
            achievement['type'] == 'totaldiff' and
            achievement['threshold'] == 5
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
    ('different_bars', 'done'),
    [
        (3, 0),
        (5, 1),
        (6, 1),
        (25, 2),
        (40, 2),
        (50, 3),
        (100, 4),
        (130, 4),
    ],
)
def test_getting_lower_achievements_if_higher_achieved(
    db, authenticated_client: APIClient, user_email, different_bars, done
):
    user = User.objects.get(email=user_email)
    upsert_achievements(
        user, achievements=TOTAL_DIFFERENT_PULL_UP_BARS_ACHIEVEMENTS
    )
    bars = make(Bars, different_bars)
    main_bar = None
    for bar in bars:
        if main_bar is None:
            main_bar = bar
            continue
        make(PullUpCounter, reps=5, bar=bar, user=user)

    payload = {
        'reps': 10
    }

    url = get_pull_up_counter_list_url(main_bar.id)
    response = authenticated_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    done_achievements = user.achievements.filter(done=True)
    assert done_achievements.count() == done
    assert Notification.objects.count() == done


def test_not_getting_same_achievement_twice(
    db, authenticated_client: APIClient, user_email
):
    user = User.objects.get(email=user_email)
    upsert_achievements(
        user, achievements=TOTAL_DIFFERENT_PULL_UP_BARS_ACHIEVEMENTS
    )
    bars = make(Bars, 5)
    main_bar = None
    for bar in bars:
        if main_bar is None:
            main_bar = bar
            continue
        make(PullUpCounter, reps=10, bar=bar, user=user)

    achievement_title = None
    for achievement in TOTAL_DIFFERENT_PULL_UP_BARS_ACHIEVEMENTS:
        if (
            achievement['type'] == 'totaldiff' and
            achievement['threshold'] == 5
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
    assert done_achievement.done is True

    response = authenticated_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    done_achievement = user.achievements.get(title=achievement_title)
    assert done_achievement.done is True


def test_0_reps_does_not_included(
    db, authenticated_client: APIClient, user_email
):
    user = User.objects.get(email=user_email)
    upsert_achievements(
        user, achievements=TOTAL_DIFFERENT_PULL_UP_BARS_ACHIEVEMENTS
    )
    bars = make(Bars, 5)
    main_bar = None
    for bar in bars:
        if main_bar is None:
            main_bar = bar
            continue
        make(PullUpCounter, reps=0, bar=bar, user=user)

    achievement_title = None
    for achievement in TOTAL_DIFFERENT_PULL_UP_BARS_ACHIEVEMENTS:
        if (
            achievement['type'] == 'totaldiff' and
            achievement['threshold'] == 5
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
