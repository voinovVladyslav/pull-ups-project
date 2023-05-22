import pytest
from rest_framework import status
from model_bakery.baker import make

from tag.models import Tag
from tests.fixtures import superuser_client, api_client
from tests.user.fixtures import (
    create_superuser, superuser_email, superuser_password
)
from .fixtures import tag_payload
from .urls import get_tags_detail_url


def test_update_tag_success(db, superuser_client):
    tag = make(Tag)

    assert Tag.objects.count() == 1

    url = get_tags_detail_url(tag.id)
    payload = {
        'name': '#update tag'
    }
    response = superuser_client.patch(url, payload, format='json')
    assert response.status_code == status.HTTP_200_OK

    tag.refresh_from_db()

    assert tag.name == payload['name']


def test_update_bars_with_empty_values_fail(db, superuser_client):
    tag = make(Tag)
    assert Tag.objects.count() == 1

    url = get_tags_detail_url(tag.id)
    payload = {
        'name': ''
    }
    response = superuser_client.patch(url, payload, format='json')

    assert response.status_code == status.HTTP_400_BAD_REQUEST
