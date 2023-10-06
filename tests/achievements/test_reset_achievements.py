from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery.baker import make

from tests.fixtures import authenticated_client, api_client
from tests.user.fixtures import create_user, user_email, user_password
from .urls import RESET_ACHIEVEMENTS_URL, get_reset_achievement_detail_url

from achievements.models import Achievement
from achievements.helpers.upsert import upsert_achievements


def test_reset_single_achievements_sets_done_to_false(
    db, authenticated_client: APIClient, user_email
):
    user = get_user_model().objects.get(email=user_email)
    achievement = make(Achievement, done=True)
    user.achievements.add(achievement)

    response = authenticated_client.post(
        get_reset_achievement_detail_url(achievement.id)
    )
    assert response.status_code == status.HTTP_200_OK
    achievement: Achievement = user.achievements.first()
    assert achievement.done is False


def test_reset_all_achievements(
    db, authenticated_client: APIClient, user_email,
):
    user = get_user_model().objects.get(email=user_email)
    upsert_achievements(user)
    user.achievements.update(done=True)

    response = authenticated_client.post(RESET_ACHIEVEMENTS_URL)
    assert response.status_code == status.HTTP_200_OK
    all_achievements = user.achievements.all().count()
    not_done_achievements = user.achievements.filter(done=False).count()
    assert all_achievements == not_done_achievements
