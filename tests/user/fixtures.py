import pytest
import uuid
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
def create_user(db, django_user_model, user_password):
    def make_user(**kwargs):
        kwargs['password'] = user_password
        if 'email' not in kwargs:
            kwargs['email'] = str(uuid.uuid4()) + '@example.com'
            return django_user_model.objects.create_user(**kwargs)
    return make_user
