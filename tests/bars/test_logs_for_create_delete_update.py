from model_bakery.baker import make

from logs.models import LogRecord
from user.models import User
from pullupbars.models import PullUpBars

from .urls import BARS_LIST_URL, get_bars_detail_url


def test_log_record_for_bars_create(
    db, superuser_client, superuser_email, bars_payload
):
    user = User.objects.get(email=superuser_email)
    assert LogRecord.objects.count() == 0
    assert PullUpBars.objects.count() == 0
    superuser_client.post(
        BARS_LIST_URL, bars_payload, format='json'
    )
    assert PullUpBars.objects.count() == 1
    assert LogRecord.objects.count() == 1
    log = LogRecord.objects.first()
    bar = PullUpBars.objects.first()
    assert log.user == user
    assert log.pullupbar == bar


def test_log_record_not_created_if_invalid_payload(
    db, superuser_client, superuser_email
):
    assert LogRecord.objects.count() == 0
    assert PullUpBars.objects.count() == 0
    superuser_client.post(
        BARS_LIST_URL, {'name': 'test'}, format='json'
    )
    assert PullUpBars.objects.count() == 0
    assert LogRecord.objects.count() == 0


def test_log_record_created_if_bars_updated(
    db, superuser_client, superuser_email, bars_payload,
):
    user = User.objects.get(email=superuser_email)
    bars = make(PullUpBars)

    assert PullUpBars.objects.count() == 1
    assert LogRecord.objects.count() == 0

    url = get_bars_detail_url(bars.id)
    superuser_client.patch(url, bars_payload, format='json')
    assert PullUpBars.objects.count() == 1
    assert LogRecord.objects.count() == 1
    log = LogRecord.objects.first()
    assert log.user == user
    assert log.pullupbar == bars


def test_log_record_not_created_if_failed_to_update_bars(
    db, superuser_client, superuser_email, bars_payload,
):
    bars = make(PullUpBars)

    assert PullUpBars.objects.count() == 1
    assert LogRecord.objects.count() == 0

    url = get_bars_detail_url(bars.id)
    response = superuser_client.patch(url, {'location': 'test'}, format='json')
    assert response.status_code != 200
    assert PullUpBars.objects.count() == 1
    assert LogRecord.objects.count() == 0


def test_log_record_created_if_bars_was_deleted(
    db, superuser_client, superuser_email
):
    user = User.objects.get(email=superuser_email)
    bars = make(PullUpBars)

    assert LogRecord.objects.count() == 0
    assert PullUpBars.objects.count() == 1

    url = get_bars_detail_url(bars.id)
    superuser_client.delete(url, format='json')
    assert PullUpBars.objects.count() == 0
    assert LogRecord.objects.count() == 1
    log = LogRecord.objects.first()
    assert log.user == user


def test_log_record_not_created_if_failed_to_delete_bars(
    db, superuser_client, superuser_email,
):
    bars = make(PullUpBars)

    assert PullUpBars.objects.count() == 1
    assert LogRecord.objects.count() == 0

    url = get_bars_detail_url(bars.id + 1)
    superuser_client.delete(url, format='json')
    assert PullUpBars.objects.count() == 1
    assert LogRecord.objects.count() == 0
