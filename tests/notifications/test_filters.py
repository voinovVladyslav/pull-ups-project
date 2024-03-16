import json

import pytest
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery.baker import make

from user.models import User
from notifications.models import Notification
from .urls import NOTIFICATIONS_URL


@pytest.mark.parametrize(
    ('count', 'unread_value'),
    [
        (3, 'true'),
        (5, 'false'),
        (8, 'test'),
        (8, ''),
        (8, 10),
    ],
    ids=[
        'Filter by unread=True',
        'Filter by unread=False',
        'Filter by unread=test',
        'Filter by unread=""',
        'Filter by unread=10',
    ]
)
def test_filter_by_unread(
    db, authenticated_client: APIClient, count, unread_value
):
    user = User.objects.first()
    make(Notification, 3, user=user, unread=True)
    make(Notification, 5, user=user, unread=False)
    url = f"{NOTIFICATIONS_URL}?unread={unread_value}"
    response = authenticated_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    data = json.loads(response.content)

    if unread_value in ['true', 'false']:
        # remove pagination when filtering
        assert len(data) == count
    else:
        assert len(data['results']) == count
