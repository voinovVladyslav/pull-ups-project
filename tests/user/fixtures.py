import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user_email():
    return 'user@example.com'


@pytest.fixture
def user_password():
    return 'testpassword'

@pytest.fixture
def user(user_password, user_email):
    return get_user_model().objects.create_user(email=user_email, password=user_password)
