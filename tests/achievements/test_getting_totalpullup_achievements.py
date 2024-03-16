import pytest

from rest_framework import status
from rest_framework.test import APIClient
from model_bakery.baker import make

from tests.counter.urls import get_pull_up_counter_list_url

from user.models import User
from pullupbars.models import PullUpBars
from counter.models import PullUpCounter
from notifications.models import Notification
from achievements.helpers.upsert import upsert_achievements
from achievements.constants import TOTAL_PULL_UP_ACHIEVEMENTS


def test_getting_achievement_for_100_total_pullups(
    db, authenticated_client: APIClient, user_email
):
    user = User.objects.get(email=user_email)
    upsert_achievements(user, achievements=TOTAL_PULL_UP_ACHIEVEMENTS)
    bar = make(PullUpBars)
    make(PullUpCounter, 11, reps=9, pullupbar=bar, user=user)

    achievement_title = None
    for achievement in TOTAL_PULL_UP_ACHIEVEMENTS:
        if (
            achievement['type'] == 'totalpullup' and
            achievement['threshold'] == 100
        ):
            achievement_title = achievement['title']
            break

    payload = {
        'reps': 5
    }

    assert Notification.objects.count() == 0
    url = get_pull_up_counter_list_url(bar.id)
    response = authenticated_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    done_achievement = user.achievements.get(title=achievement_title)
    assert done_achievement.done is True
    assert Notification.objects.count() == 1


@pytest.mark.parametrize(
    ('reps_total', 'done'),
    [
        (50, 0),
        (99, 1),
        (499, 2),
        (999, 3),
        (4999, 4),
        (6000, 4),
        (8999, 5),
        (14999, 6),
        (17000, 6),
    ],
)
def test_getting_lower_achievements_if_higher_achieved(
    db, authenticated_client: APIClient, user_email, reps_total, done
):
    user = User.objects.get(email=user_email)
    upsert_achievements(user, achievements=TOTAL_PULL_UP_ACHIEVEMENTS)
    bar = make(PullUpBars)
    make(PullUpCounter, reps=reps_total, pullupbar=bar, user=user)

    payload = {
        'reps': 10
    }

    url = get_pull_up_counter_list_url(bar.id)
    response = authenticated_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    done_achievements = user.achievements.filter(done=True)
    assert done_achievements.count() == done
    assert Notification.objects.count() == done


def test_not_getting_same_achievement_twice(
    db, authenticated_client: APIClient, user_email
):
    user = User.objects.get(email=user_email)
    upsert_achievements(user, achievements=TOTAL_PULL_UP_ACHIEVEMENTS)
    bar = make(PullUpBars)
    make(PullUpCounter, 11, reps=9, pullupbar=bar, user=user)

    payload = {
        'reps': 6
    }

    url = get_pull_up_counter_list_url(bar.id)
    response = authenticated_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    done_achievements = user.achievements.filter(done=True)
    assert done_achievements.count() == 1

    response = authenticated_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    done_achievements = user.achievements.filter(done=True)
    assert done_achievements.count() == 1
