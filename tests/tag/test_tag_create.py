import pytest
from rest_framework import status

from tag.models import Tag
from tests.fixtures import api_client, superuser_client
from .fixtures import tag_payload
from tests.user.fixtures import (
    create_superuser, superuser_email, superuser_password
)
from .urls import TAG_LIST_URL


def test_create_tag_success(db, superuser_client, tag_payload):
    assert Tag.objects.count() == 0
    responce = superuser_client.post(TAG_LIST_URL, tag_payload, format='json')
    assert responce.status_code == status.HTTP_201_CREATED
    assert Tag.objects.count() == 1


def test_create_tags_with_blank_values_fail(db, superuser_client):
    assert Tag.objects.count() == 0
    payload = {
        'name': ''
    }
    response = superuser_client.post(TAG_LIST_URL, payload, format='json')
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert Tag.objects.count() == 0
