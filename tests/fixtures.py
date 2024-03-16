import pytest
from rest_framework.test import APIClient


@pytest.fixture()
def api_client():
    return APIClient()


@pytest.fixture()
def authenticated_client(db, create_user, api_client):
    user = create_user()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)


@pytest.fixture()
def superuser_client(
    db, create_superuser, api_client
):
    user = create_superuser()
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)
