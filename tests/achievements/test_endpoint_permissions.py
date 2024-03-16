import pytest
from rest_framework import status
from rest_framework.test import APIClient

from .urls import ACHIEVEMENTS_LIST_URL


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
def test_allowed_methods(
        db, authenticated_client, method_name, response_code
):
    response = getattr(authenticated_client, method_name)(
        ACHIEVEMENTS_LIST_URL
    )
    assert response.status_code == response_code


@pytest.mark.parametrize(
    'method_name,response_code',
    [
        ('get', status.HTTP_401_UNAUTHORIZED),
        ('post', status.HTTP_401_UNAUTHORIZED),
        ('put', status.HTTP_401_UNAUTHORIZED),
        ('patch', status.HTTP_401_UNAUTHORIZED),
        ('delete', status.HTTP_401_UNAUTHORIZED),
    ],
    ids=[
        'GET NOT ALLOWED',
        'POST NOT ALLOWED',
        'PUT NOT ALLOWED',
        'PATCH NOT ALLOWED',
        'DELETE NOT ALLOWED',
    ]
)
def test_not_allowed_access_without_authentication(
        db, api_client: APIClient, method_name, response_code
):
    response = getattr(api_client, method_name)(ACHIEVEMENTS_LIST_URL)
    assert response.status_code == response_code


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
def test_read_only_for_authenticated_user(
        db, authenticated_client: APIClient, method_name, response_code
):
    response = getattr(authenticated_client, method_name)(
        ACHIEVEMENTS_LIST_URL
    )
    assert response.status_code == response_code
