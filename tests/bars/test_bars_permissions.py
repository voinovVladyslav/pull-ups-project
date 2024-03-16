import pytest
from rest_framework import status


from .urls import BARS_LIST_URL, get_bars_detail_url


@pytest.mark.parametrize(
    'method_name,response_code',
    [
        ('get', status.HTTP_200_OK),
        ('post', status.HTTP_403_FORBIDDEN),
        ('put', status.HTTP_403_FORBIDDEN),
        ('patch', status.HTTP_403_FORBIDDEN),
        ('delete', status.HTTP_403_FORBIDDEN),
    ],
    ids=[
        'GET ALLOWED',
        'POST NOT ALLOWED',
        'PUT NOT ALLOWED',
        'PATCH NOT ALLOWED',
        'DELETE NOT ALLOWED',
    ]
)
def test_only_get_allowed_for_list_view_for_authenticated_user(
        db, authenticated_client, method_name, response_code
):
    response = getattr(authenticated_client, method_name)(BARS_LIST_URL)
    assert response.status_code == response_code


@pytest.mark.parametrize(
    'method_name,response_code',
    [
        ('get', status.HTTP_404_NOT_FOUND),
        ('post', status.HTTP_403_FORBIDDEN),
        ('put', status.HTTP_403_FORBIDDEN),
        ('patch', status.HTTP_403_FORBIDDEN),
        ('delete', status.HTTP_403_FORBIDDEN),
    ],
    ids=[
        'GET ALLOWED',
        'POST NOT ALLOWED',
        'PUT NOT ALLOWED',
        'PATCH NOT ALLOWED',
        'DELETE NOT ALLOWED',
    ]
)
def test_only_get_allowed_for_authenticated_user(
        db, authenticated_client, method_name, response_code
):
    response = getattr(
        authenticated_client, method_name
    )(get_bars_detail_url(1))
    assert response.status_code == response_code


@pytest.mark.parametrize(
    'method_name,response_code',
    [
        ('get', status.HTTP_200_OK),
        ('post', status.HTTP_401_UNAUTHORIZED),
        ('put', status.HTTP_401_UNAUTHORIZED),
        ('patch', status.HTTP_401_UNAUTHORIZED),
        ('delete', status.HTTP_401_UNAUTHORIZED),
    ],
    ids=[
        'GET ALLOWED',
        'POST NOT ALLOWED',
        'PUT NOT ALLOWED',
        'PATCH NOT ALLOWED',
        'DELETE NOT ALLOWED',
    ]
)
def test_only_get_allowed_for_list_view_for_unauthenticated_user(
        db, api_client, method_name, response_code
):
    response = getattr(api_client, method_name)(BARS_LIST_URL)
    assert response.status_code == response_code


@pytest.mark.parametrize(
    'method_name,response_code',
    [
        ('get', status.HTTP_404_NOT_FOUND),
        ('post', status.HTTP_401_UNAUTHORIZED),
        ('put', status.HTTP_401_UNAUTHORIZED),
        ('patch', status.HTTP_401_UNAUTHORIZED),
        ('delete', status.HTTP_401_UNAUTHORIZED),
    ],
    ids=[
        'GET ALLOWED',
        'POST NOT ALLOWED',
        'PUT NOT ALLOWED',
        'PATCH NOT ALLOWED',
        'DELETE NOT ALLOWED',
    ]
)
def test_get_put_patch_delete_allowed_for_unauthenticated_user(
        db, api_client, method_name, response_code
):
    response = getattr(api_client, method_name)(get_bars_detail_url(1))
    assert response.status_code == response_code
