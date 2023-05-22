from rest_framework import status
from model_bakery.baker import make

from tag.models import Tag
from tests.fixtures import superuser_client, api_client
from tests.user.fixtures import (
    create_superuser, superuser_email, superuser_password
)
from .fixtures import tag_payload
from .urls import get_tags_detail_url


def test_delete_success(db, superuser_client):
    tag = make(Tag)
    Tag.objects.count() == 1
    url = get_tags_detail_url(tag.id)
    response = superuser_client.delete(url, format='json')
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Tag.objects.count() == 0


def test_delete_nonexisting_tag_fail(db, superuser_client):
    tag = make(Tag)
    assert Tag.objects.count() == 1
    url = get_tags_detail_url(tag.id + 1)
    response = superuser_client.delete(url, format='json')
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert Tag.objects.count() == 1
