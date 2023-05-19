import pytest
from rest_framework import status


from .urls import BARS_LIST_URL, get_bars_detail_url
from tests.user.fixtures import (
    superuser_email, superuser_password, create_superuser
)
from tests.fixtures import superuser_client, api_client


@pytest.mark.parametrize(
    'method_name,response_code',
    [
        ('get', status.HTTP_200_OK),
        ('post', status.HTTP_400_BAD_REQUEST),
        ('put', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('patch', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('delete', status.HTTP_405_METHOD_NOT_ALLOWED),
    ],
    ids=[
        'GET ALLOWED',
        'POST ALLOWED',
        'PUT NOT ALLOWED',
        'PATCH NOT ALLOWED',
        'DELETE NOT ALLOWED',
    ]
)
def test_only_get_post_allowed_for_list_view(
        db, superuser_client, method_name, response_code
):
    response = getattr(superuser_client, method_name)(BARS_LIST_URL)
    assert response.status_code == response_code


@pytest.mark.parametrize(
    'method_name,response_code',
    [
        ('get', status.HTTP_404_NOT_FOUND),
        ('post', status.HTTP_405_METHOD_NOT_ALLOWED),
        ('put', status.HTTP_404_NOT_FOUND),
        ('patch', status.HTTP_404_NOT_FOUND),
        ('delete', status.HTTP_404_NOT_FOUND),
    ],
    ids=[
        'GET ALLOWED',
        'POST NOT ALLOWED',
        'PUT ALLOWED',
        'PATCH ALLOWED',
        'DELETE ALLOWED',
    ]
)
def test_get_put_patch_delete_allowed(
        db, superuser_client, method_name, response_code
):
    response = getattr(superuser_client, method_name)(get_bars_detail_url(1))
    assert response.status_code == response_code
