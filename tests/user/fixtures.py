import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_email():
    return 'user@example.com'


@pytest.fixture
def user_password():
    return 'testpassword'
