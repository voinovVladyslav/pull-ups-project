import pytest
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model

from .fixtures import api_client, user_email, user_password
from .urls import CREATE_USER_URL


def test_create_user_success(
        db, api_client: APIClient, user_email, user_password
):
    payload = {
        'email': user_email,
        'password': user_password,
    }
    response = api_client.post(CREATE_USER_URL, data=payload)
    assert response.status_code == status.HTTP_201_CREATED
    user = get_user_model().objects.first()
    assert user.email == user_email
    assert user.check_password(user_password)


def test_create_user_with_existing_email_fail(
        db, api_client: APIClient, user_email, user_password
):
    user = get_user_model().objects.create_user(user_email, user_password)
    payload = {
        'email': user_email,
        'password': user_password,
    }
    response = api_client.post(CREATE_USER_URL, data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert get_user_model().objects.count() == 1


def test_create_user_without_password_fail(
        db, api_client: APIClient, user_email
):
    user = get_user_model()
    payload = {
        'email': user_email,
        'password':''
    }
    response = api_client.post(CREATE_USER_URL, data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert get_user_model().objects.count() == 0


def test_create_user_with_existing_password_success(
        db, api_client: APIClient, user_password
):
    user = get_user_model()
    user_email_1 = 'test1@gmail.com'
    user_email_2 = 'test2@gmail.com'
    user.objects.create_user(user_email_1, user_password)
    payload = {
        'email': user_email_2,
        'password': user_password,
    }
    response = api_client.post(CREATE_USER_URL, data=payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert get_user_model().objects.count() == 2


def test_create_user_without_data_fail(
        db, api_client: APIClient
):
    user = get_user_model()
    payload = {
        'email': '',
        'password':''
    }
    response = api_client.post(CREATE_USER_URL, data=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert get_user_model().objects.count() == 0


@pytest.mark.parametrize(
    'email_name,response_code',
    [
        ('usergmail.com', status.HTTP_400_BAD_REQUEST),
        ('user@gmailcom', status.HTTP_400_BAD_REQUEST),
        ('user gmail@gmail.com', status.HTTP_400_BAD_REQUEST),
        ('user@gmail..com', status.HTTP_400_BAD_REQUEST),
        ('user@gmail_com', status.HTTP_400_BAD_REQUEST),
        ('юзер@gmail.com', status.HTTP_400_BAD_REQUEST),
    ],
    ids=[
        'MISSING @ SYMBOL',
        'MISSING DOT IN TOP-LEVEL DOMAIN',
        'SPACE USAGE',
        'INVALID DOMAIN FORMAT',
        'USE OF FORBIDDEN CHARACTER',
        'WITH CYRILLIC CHARACTERS'
    ]
)
def test_create_user_wrong_emails_fail(
        db,
        api_client: APIClient,
        user_password,
        email_name,
        response_code,
):
    payload = {
        'email': email_name,
        'password':user_password
    }
    response = api_client.post(CREATE_USER_URL, data=payload)
    assert response.status_code == response_code
    assert get_user_model().objects.count() == 0


@pytest.mark.parametrize(
    'method_name,response_code,n_of_users',
    [
        ('get', status.HTTP_405_METHOD_NOT_ALLOWED, 0),
        ('put', status.HTTP_405_METHOD_NOT_ALLOWED, 0),
        ('patch', status.HTTP_405_METHOD_NOT_ALLOWED, 0),
        ('delete', status.HTTP_405_METHOD_NOT_ALLOWED, 0),
        ('post', status.HTTP_201_CREATED, 1),
    ],
    ids=[
        'GET NOT ALLOWED',
        'PUT NOT ALLOWED',
        'PATCH NOT ALLOWED',
        'DELETE NOT ALLOWED',
        'POST ALLOWED',
    ]
)
def test_allowed_methods_for_create_user(
        db,
        api_client: APIClient,
        user_email,
        user_password,
        method_name,
        response_code,
        n_of_users,
):
    payload = {
        'email': user_email,
        'password': user_password,
    }
    response = getattr(api_client, method_name)(CREATE_USER_URL, data=payload)
    assert response.status_code == response_code
    assert get_user_model().objects.count() == n_of_users
