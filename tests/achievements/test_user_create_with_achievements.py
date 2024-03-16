from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from tests.user.urls import CREATE_USER_URL


def test_user_created_with_all_achievements_linked(
    db, api_client: APIClient, user_email, user_password, number_of_achievemnts
):
    payload = {
        'email': user_email,
        'password': user_password,
    }
    response = api_client.post(CREATE_USER_URL, data=payload)
    assert response.status_code == status.HTTP_201_CREATED
    user = get_user_model().objects.get(email=user_email)
    assert user.achievements.count() == number_of_achievemnts
