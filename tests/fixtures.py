import pytest
from rest_framework.test import APIClient

from tests.user.fixtures import create_user, user_email, user_password


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def authenticated_client(db, create_user, api_client):
    user = create_user()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)
