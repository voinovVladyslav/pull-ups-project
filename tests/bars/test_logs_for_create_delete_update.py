import pytest
from model_bakery.baker import make

from logs.models import LogRecord
from user.models import User
from bars.models import Bars

from .urls import BARS_LIST_URL, get_bars_detail_url
from tests.user.fixtures import (
    superuser_email, superuser_password, create_superuser
)
from tests.bars.fixtures import bars_payload
from tests.fixtures import superuser_client, api_client


def test_log_record_for_bars_create(
    db, superuser_client, superuser_email, bars_payload
):
    user = User.objects.get(email=superuser_email)
    assert LogRecord.objects.count() == 0
    assert Bars.objects.count() == 0
    response = superuser_client.post(
        BARS_LIST_URL, bars_payload, format='json'
    )
    assert Bars.objects.count() == 1
    assert LogRecord.objects.count() == 1
    log = LogRecord.objects.first()
    bar = Bars.objects.first()
    assert log.user == user
    assert log.bar == bar


def test_log_record_not_created_if_invalid_payload(
    db, superuser_client, superuser_email
):
    user = User.objects.get(email=superuser_email)
    assert LogRecord.objects.count() == 0
    assert Bars.objects.count() == 0
    response = superuser_client.post(
        BARS_LIST_URL, {'name': 'test'}, format='json'
    )
    assert Bars.objects.count() == 0
    assert LogRecord.objects.count() == 0


def test_log_record_created_if_bars_updated(
    db, superuser_client, superuser_email, bars_payload,
):
    user = User.objects.get(email=superuser_email)
    bars = make(Bars)

    assert Bars.objects.count() == 1
    assert LogRecord.objects.count() == 0

    url = get_bars_detail_url(bars.id)
    response = superuser_client.patch(url, bars_payload, format='json')
    assert Bars.objects.count() == 1
    assert LogRecord.objects.count() == 1
    log = LogRecord.objects.first()
    assert log.user == user
    assert log.bar == bars


def test_log_record_not_created_if_failed_to_update_bars(
    db, superuser_client, superuser_email, bars_payload,
):
    user = User.objects.get(email=superuser_email)
    bars = make(Bars)

    assert Bars.objects.count() == 1
    assert LogRecord.objects.count() == 0

    url = get_bars_detail_url(bars.id)
    response = superuser_client.patch(url, {'location': 'test'}, format='json')
    assert response.status_code != 200
    assert Bars.objects.count() == 1
    assert LogRecord.objects.count() == 0


def test_log_record_created_if_bars_was_deleted(
    db, superuser_client, superuser_email
):
    user = User.objects.get(email=superuser_email)
    bars = make(Bars)

    assert LogRecord.objects.count() == 0
    assert Bars.objects.count() == 1

    url = get_bars_detail_url(bars.id)
    response = superuser_client.delete(url, format='json')
    assert Bars.objects.count() == 0
    assert LogRecord.objects.count() == 1
    log = LogRecord.objects.first()
    assert log.user == user


def test_log_record_not_created_if_failed_to_delete_bars(
    db, superuser_client, superuser_email,
):
    bars = make(Bars)

    assert Bars.objects.count() == 1
    assert LogRecord.objects.count() == 0

    url = get_bars_detail_url(bars.id + 1)
    response = superuser_client.delete(url, format='json')
    assert Bars.objects.count() == 1
    assert LogRecord.objects.count() == 0
