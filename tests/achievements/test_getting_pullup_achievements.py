import pytest

from rest_framework import status
from rest_framework.test import APIClient
from model_bakery.baker import make

from tests.fixtures import api_client, authenticated_client
from tests.user.fixtures import create_user, user_email, user_password
from tests.counter.urls import get_pull_up_counter_list_url
from .urls import ACHIEVEMENTS_LIST_URL

from user.models import User
from bars.models import Bars
from counter.models import PullUpCounter
from achievements.helpers.upsert import upsert_achievements
from achievements.constants import PULLUP_ACHIEVEMENTS


def test_getting_achievement_for_5_pullups(
    db, authenticated_client: APIClient, user_email
):
    user = User.objects.get(email=user_email)
    upsert_achievements(user, achievements=PULLUP_ACHIEVEMENTS)
    bar = make(Bars)

    for achievement in PULLUP_ACHIEVEMENTS:
        if achievement['id'] == 'pullup5':
            achievement_title = achievement['title']

    payload = {
        'reps': 5
    }

    url = get_pull_up_counter_list_url(bar.id)
    response = authenticated_client.post(url, payload)
    assert response.status_code == status.HTTP_200_OK
    done_achievement = user.achievements.filter(title=achievement_title)
    assert done_achievement.done is True


@pytest.mark.parametrize(
    'reps,done',
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
    bar = make(Bars)

    payload = {
        'reps': reps
    }

    url = get_pull_up_counter_list_url(bar.id)
    response = authenticated_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    done_achievements = user.achievements.filter(done=True)
    assert done_achievements.count() == done
