import pytest
from rest_framework import status
from model_bakery.baker import make

from bars.models import Bars
from tag.models import Tag
from .urls import get_bars_detail_url
from tests.user.fixtures import (
    superuser_email, superuser_password, create_superuser
)
from tests.fixtures import superuser_client, api_client


def test_set_tags_to_bars_success(superuser_client):
    bar = make(Bars)
    assert Tag.objects.count() == 0

    payload = {
        'tags': [
            {
                'name': 'test_tag_1',
            },
            {
                'name': 'test_tag_2'
            }
        ]
    }
    url = get_bars_detail_url(bar.id)
    response = superuser_client.patch(url, payload, format='json')
    bar.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert Tag.objects.count() == 2
    assert bar.tags.count() == 2


def test_update_bars_with_tags_with_empty_tags_removes_tags_from_bars(
    superuser_client
):
    bar = make(Bars)
    tags = make(Tag, 3)
    bar.tags.set(tags)
    assert bar.tags.count() == 3

    payload = {
        'tags': []
    }
    url = get_bars_detail_url(bar.id)
    response = superuser_client.patch(url, payload, format='json')
    bar.refresh_from_db()

    assert response.status_code == status.HTTP_200_OK
    assert Tag.objects.count() == 3
    assert bar.tags.count() == 0


def test_add_tag_with_existing_name_do_not_create_new_tag(superuser_client):
    bar = make(Bars)
    tag = Tag.objects.create(name='test_name')
    assert Tag.objects.count() == 1
    assert bar.tags.count() == 0

    payload = {
        'tags': [
            {
                'name': 'test_name'
            }
        ]
    }
    url = get_bars_detail_url(bar.id)
    response = superuser_client.patch(url, payload, format='json')

    assert response.status_code == status.HTTP_200_OK
    bar.refresh_from_db()
    assert bar.tags.count() == 1
    assert Tag.objects.count() == 1


def test_add_tag_without_listing_old_removes_old_tag(superuser_client):
    bar = make(Bars)
    old_tag = Tag.objects.create(name='old_tag')
    new_tag = Tag.objects.create(name='new_tag')
    bar.tags.add(old_tag)

    assert old_tag in bar.tags.all()
    assert bar.tags.count() == 1

    payload = {
        'tags': [
            {
                'name': 'new_tag'
            }
        ]
    }
    url = get_bars_detail_url(bar.id)
    response = superuser_client.patch(url, payload, format='json')

    assert response.status_code == status.HTTP_200_OK
    bar.refresh_from_db()
    assert bar.tags.count() == 1
    assert old_tag not in bar.tags.all()
    assert new_tag in bar.tags.all()
