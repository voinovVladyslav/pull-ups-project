import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from .fixtures import api_client, user_email, user_password, create_user
from .urls import LOGIN_USER_URL


def test_login_user_succcess(
        db, api_client: APIClient, user_password, create_user
):
    user = create_user()
    payload = {
        'email': user.email,
        'password': user_password,
    }
    response = api_client.post(LOGIN_USER_URL, data=payload)
    assert response.status_code == status.HTTP_200_OK
    assert Token.objects.get(user=user).key == response.json()['token']


def test_login_user_nonexistent_email(
        db, api_client: APIClient, user_password, user_email
):
    payload = {
        'email': user_email,
        'password': user_password,
    }
    response = api_client.post(LOGIN_USER_URL, data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_with_missing_email_or_password(
        db, api_client: APIClient, create_user
):
    user = create_user()
    payload = {
        'email': user.email,
        'password': '',
    }
    response = api_client.post(LOGIN_USER_URL, data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.parametrize(
    'method_name,response_code',
    [
        ('get', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('put', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('patch', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('delete', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('post', status.HTTP_200_OK),
    ],
    ids=[
        'GET NOT ALLOWED',
        'PUT NOT ALLOWED',
        'PATCH NOT ALLOWED',
        'DELETE NOT ALLOWED',
        'POST ALLOWED',
    ]
)
def test_allowed_methods_for_login_user(
        db,
        api_client: APIClient,
        user_password,
        method_name,
        response_code,
        create_user,
):
    user = create_user()
    payload = {
        'email': user.email,
        'password': user_password,
    }
    response = getattr(api_client, method_name)(LOGIN_USER_URL, data=payload)
    assert response.status_code == response_code
