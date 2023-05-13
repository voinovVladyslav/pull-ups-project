import pytest
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model

from .fixtures import api_client, user_email, user_password, user
from .urls import LOGIN_USER_URL


def test_login_user_succcess(db, api_client: APIClient, user, user_password):
    payload = {
        'email': user.email,
        'password': user_password,
    }
    response = api_client.post(LOGIN_USER_URL, data=payload)
    assert response.status_code == status.HTTP_200_OK
    assert Token.objects.get(user=user).key == response.json()['token']


def test_login_user_nonexistent_email(db, api_client: APIClient, user_password, user_email):
    payload = {
        'email': user_email,
        'password': user_password,
    }
    response = api_client.post(LOGIN_USER_URL, data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


def test_login_with_missing_email_or_password(db, api_client: APIClient, user):
    payload = {
        'email': user.email,
        'password': '',
    }
    response = api_client.post(LOGIN_USER_URL, data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
