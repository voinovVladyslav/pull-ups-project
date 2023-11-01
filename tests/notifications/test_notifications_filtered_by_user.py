import json

from rest_framework import status
from rest_framework.test import APIClient
from model_bakery.baker import make

from user.models import User
from notifications.models import Notification
from tests.fixtures import api_client, authenticated_client
from tests.user.fixtures import create_user, user_email, user_password
from .urls import NOTIFICATIONS_URL


def test_notifications_filtered_by_user(
    db, authenticated_client: APIClient,
):
    authenticated_user = User.objects.first()
    other_user = User.objects.create(email='test@example.com')
    make(Notification, 5, user=other_user)
    make(Notification, 5, user=authenticated_user)

    response = authenticated_client.get(NOTIFICATIONS_URL)
    assert response.status_code == status.HTTP_200_OK
    data = json.loads(response.content)
    assert len(data['results']) == 5
