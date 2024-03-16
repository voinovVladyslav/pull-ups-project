import pytest

from rest_framework import status
from rest_framework.test import APIClient
from model_bakery.baker import make

from tests.counter.urls import get_pull_up_counter_list_url

from user.models import User
from pullupbars.models import PullUpBars
from notifications.models import Notification
from achievements.helpers.upsert import upsert_achievements
from achievements.constants import PULLUP_ACHIEVEMENTS


def test_getting_achievement_for_5_pullups(
    db, authenticated_client: APIClient, user_email
):
    user = User.objects.get(email=user_email)
    upsert_achievements(user, achievements=PULLUP_ACHIEVEMENTS)
    bar = make(PullUpBars)

    for achievement in PULLUP_ACHIEVEMENTS:
        if achievement['type'] == 'pullup' and achievement['threshold'] == 5:
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
    ('reps', 'done'),
    [
        (3, 0),
        (5, 1),
        (10, 2),
        (15, 3),
        (20, 4),
        (29, 5),
        (30, 6),
        (35, 7),
        (40, 8),
        (45, 9),
        (50, 10),
        (55, 10),
    ],
)
def test_getting_lower_achievements_if_higher_achieved(
    db, authenticated_client: APIClient, user_email, reps, done
):
    user = User.objects.get(email=user_email)
    upsert_achievements(user, achievements=PULLUP_ACHIEVEMENTS)
    bar = make(PullUpBars)

    payload = {
        'reps': reps
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
    upsert_achievements(user, achievements=PULLUP_ACHIEVEMENTS)
    bar = make(PullUpBars)

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
