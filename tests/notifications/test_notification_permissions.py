import pytest
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery.baker import make

from user.models import User
from notifications.models import Notification
from tests.fixtures import api_client, authenticated_client
from tests.user.fixtures import user_email, user_password, create_user
from .urls import NOTIFICATIONS_URL


def test_unauthenticated_client_access_denied(
    db, api_client: APIClient
):
    response = api_client.get(NOTIFICATIONS_URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_authenticated_user_access_allowed(
    db, authenticated_client: APIClient
):
    response = authenticated_client.get(NOTIFICATIONS_URL)
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.parametrize(
    'method_name,response_code',
    [
        ('get', status.HTTP_200_OK),
        ('post', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('put', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('patch', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('delete', status.HTTP_405_METHOD_NOT_ALLOWED),
    ],
    ids=[
        'GET ALLOWED',
        'POST NOT ALLOWED',
        'PUT NOT ALLOWED',
        'PATCH NOT ALLOWED',
        'DELETE NOT ALLOWED',
    ]
)
def test_allowed_methods_for_list_view(
    db, authenticated_client, method_name, response_code
):
    response = getattr(authenticated_client, method_name)(NOTIFICATIONS_URL)
    assert response.status_code == response_code
