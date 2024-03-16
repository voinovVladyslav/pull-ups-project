import pytest
from rest_framework import status
from django.contrib.auth import get_user_model

from .urls import ME_URL


def test_auth_required_for_profile_access(db, api_client):
    response = api_client.get(ME_URL)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_return_email_of_authenticated_user(
        db, authenticated_client, user_email
):
    response = authenticated_client.get(ME_URL)
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['email'] == user_email


def test_returns_only_authenticated_user_data(
        db, authenticated_client, user_email, create_user, user_password
):
    test_user = create_user(email='test_user@example.com')
    response = authenticated_client.get(ME_URL)
    assert response.status_code == status.HTTP_200_OK
    assert test_user.email not in response.content.decode()


def test_update_email_only_successfully(
    db, authenticated_client, user_email, user_password, create_user
):
    user = get_user_model().objects.get(email=user_email)
    new_email = 'new@example.com'
    payload = {
        'email': new_email,
    }
    response = authenticated_client.patch(ME_URL, payload)
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.email == new_email


def test_update_email_only_failed(
    db, authenticated_client, user_email, user_password, create_user
):
    user = get_user_model().objects.get(email=user_email)
    new_email = 'example.com'
    payload = {
        'email': new_email,
    }
    response = authenticated_client.patch(ME_URL, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    user.refresh_from_db()
    assert user.email != new_email


def test_update_password_only_successfully(
        db, authenticated_client, user_email, user_password, create_user
):
    user = get_user_model().objects.get(email=user_email)
    new_password = 'newstrongerpassword'
    payload = {
        'password': new_password
    }
    response = authenticated_client.patch(ME_URL, payload)
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.check_password(new_password)


def test_update_password_only_error(
        db, authenticated_client, user_email, user_password, create_user
):
    user = get_user_model().objects.get(email=user_email)
    new_password = 'n'
    payload = {
        'password': new_password
    }
    response = authenticated_client.patch(ME_URL, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    user.refresh_from_db()
    assert user.check_password(new_password) is False


def test_update_email_and_password_success(
        db, authenticated_client, user_email, user_password, create_user
):
    user = get_user_model().objects.get(email=user_email)
    new_password = 'newstrongpass'
    new_email = 'new@example.com'
    payload = {
        'email': new_email,
        'password': new_password
    }
    response = authenticated_client.patch(ME_URL, payload)
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.email == new_email
    assert user.check_password(new_password)


@pytest.mark.parametrize(
    ('method_name', 'response_code'),
    [
        ('get', status.HTTP_200_OK),
        ('put', status.HTTP_200_OK),
        ('patch', status.HTTP_200_OK),
        ('delete', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('post', status.HTTP_405_METHOD_NOT_ALLOWED),
    ],
    ids=[
        'GET allowed',
        'PUT allowed',
        'PATCH allowed',
        'DELETE not allowed',
        'POST not allowed',
    ]
)
def test_allowed_methods_for_user_profile(
        db,
        authenticated_client,
        user_email,
        user_password,
        method_name,
        response_code,
):
    payload = {
        'email': user_email,
        'password': user_password,
    }
    response = getattr(authenticated_client, method_name)(ME_URL, data=payload)
    assert response.status_code == response_code
