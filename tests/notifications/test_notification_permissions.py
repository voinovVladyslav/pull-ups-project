from rest_framework import status
from rest_framework.test import APIClient
from model_bakery.baker import make

from user.models import User
from notifications.models import Notification
from tests.fixtures import api_client, authenticated_client
from tests.user.fixtures import user_email, user_password, create_user
from .urls import NOTIFICATIONS_URL, get_notification_detail_url


def test_unauthenticated_client_access_denied(
    db, api_client: APIClient, create_user
):
    user = create_user()
    notification = make(Notification, user=user)
    response = api_client.get(NOTIFICATIONS_URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    detail_response = api_client.get(
        get_notification_detail_url(notification.pk)
    )
    assert detail_response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authenticated_user_access_allowed(
    db, authenticated_client: APIClient
):
    user = User.objects.first()
    notification = make(Notification, user=user)
    response = authenticated_client.get(NOTIFICATIONS_URL)
    assert response.status_code == status.HTTP_200_OK
    detail_response = authenticated_client.get(
        get_notification_detail_url(notification.pk)
    )
    assert detail_response.status_code == status.HTTP_200_OK
