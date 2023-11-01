import json

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery.baker import make

from user.models import User
from notifications.models import Notification
from tests.fixtures import api_client, authenticated_client
from tests.user.fixtures import create_user, user_email, user_password
from .urls import NOTIFICATIONS_URL


@pytest.mark.parametrize(
    'count,unread_value',
    [
        (3, True),
        (5, False),
    ],
    ids=[
        'Filter by unread=True',
        'Filter by unread=False',
    ]
)
def test_filter_by_unread(
    db, authenticated_client: APIClient, count, unread_value
):
    user = User.objects.first()
    make(Notification, 3, user=user, unread=True)
    make(Notification, 5, user=user, unread=False)
    params = {
        'unread': unread_value,
    }
    response = authenticated_client.get(NOTIFICATIONS_URL, params=params)
    assert response.status_code == status.HTTP_200_OK
    data = json.loads(response.content)
    assert len(data['results']) == count
