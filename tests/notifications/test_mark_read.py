import json

from rest_framework import status
from rest_framework.test import APIClient
from model_bakery.baker import make

from user.models import User
from notifications.models import Notification
from .urls import MARK_READ_URL


def test_mark_notifications_as_read_set_unread_to_false(
    db, authenticated_client: APIClient
):
    user = User.objects.first()
    notification = make(Notification, user=user, unread=True)
    response = authenticated_client.post(MARK_READ_URL)
    assert response.status_code == status.HTTP_200_OK
    data = json.loads(response.content)
    assert data['marked_as_read'] == 1
    notification.refresh_from_db()
    assert notification.unread is False
