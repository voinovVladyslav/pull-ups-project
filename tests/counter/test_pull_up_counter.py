from rest_framework import status
from model_bakery.baker import make

from counter.models import PullUpCounter
from pullupbars.models import PullUpBars
from user.models import User
from .urls import get_pull_up_counter_detail_url, get_pull_up_counter_list_url


def test_authentication_required(
    db, api_client, create_user
):
    bar = make(PullUpBars)
    user = create_user()
    make(PullUpCounter, pullupbar=bar, user=user)

    url = get_pull_up_counter_list_url(bar.id)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_return_only_user_related_counter(
    db, superuser_client, superuser_email, create_user
):
    bar = make(PullUpBars)
    user = User.objects.get(email=superuser_email)
    second_user = create_user()
    make(PullUpCounter, 5, user=user, pullupbar=bar)
    make(PullUpCounter, 5, user=second_user, pullupbar=bar)
    assert PullUpCounter.objects.count() == 10

    url = get_pull_up_counter_list_url(bar.id)
    response = superuser_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_counters = response.data
    assert len(response_counters) + 1 == 5


def test_create_counter(db, superuser_client, superuser_email):
    bar = make(PullUpBars)
    user = User.objects.get(email=superuser_email)
    payload = {
        'reps': 10,
    }
    assert PullUpCounter.objects.count() == 0
    url = get_pull_up_counter_list_url(bar.id)
    response = superuser_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert PullUpCounter.objects.count() == 1
    counter = PullUpCounter.objects.first()
    assert counter.reps == payload['reps']
    assert counter.user == user
    assert counter.pullupbar == bar


def test_create_counter_invalid_bars_id(db, superuser_client):
    bar = make(PullUpBars)
    payload = {
        'reps': 10,
    }
    assert PullUpCounter.objects.count() == 0
    url = get_pull_up_counter_list_url(bar.id + 1)
    response = superuser_client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert PullUpCounter.objects.count() == 0


def test_update_counter(db, superuser_client, superuser_email):
    bar = make(PullUpBars)
    user = User.objects.get(email=superuser_email)
    counter = make(PullUpCounter, user=user, pullupbar=bar, reps=10)
    payload = {
        'reps': 20
    }
    url = get_pull_up_counter_detail_url(bar.id, counter.id)
    response = superuser_client.patch(url, payload)
    assert response.status_code == status.HTTP_200_OK
    counter.refresh_from_db()
    assert counter.reps == payload['reps']


def test_update_counter_invalid_payload(db, superuser_client, superuser_email):
    bar = make(PullUpBars)
    user = User.objects.get(email=superuser_email)
    reps = 10
    counter = make(PullUpCounter, user=user, pullupbar=bar, reps=reps)
    payload = {
        'reps': 'hello'
    }
    url = get_pull_up_counter_detail_url(bar.id, counter.id)
    response = superuser_client.patch(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    counter.refresh_from_db()
    assert counter.reps == reps


def test_delete_counter(db, superuser_client, superuser_email):
    bar = make(PullUpBars)
    user = User.objects.get(email=superuser_email)
    counter = make(PullUpCounter, user=user, pullupbar=bar)
    assert PullUpCounter.objects.count() == 1

    url = get_pull_up_counter_detail_url(bar.id, counter.id)
    response = superuser_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert PullUpCounter.objects.count() == 0


def test_delete_counter_invalid_id(db, superuser_client, superuser_email):
    bar = make(PullUpBars)
    user = User.objects.get(email=superuser_email)
    counter = make(PullUpCounter, user=user, pullupbar=bar)
    assert PullUpCounter.objects.count() == 1

    url = get_pull_up_counter_detail_url(bar.id, counter.id + 1)
    response = superuser_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert PullUpCounter.objects.count() == 1


def test_delete_counter_using_different_bars_id_result_in_error(
    db, superuser_client, superuser_email,
):
    bar, bar2 = make(PullUpBars, 2)
    user = User.objects.get(email=superuser_email)
    counter = make(PullUpCounter, user=user, pullupbar=bar)
    assert PullUpCounter.objects.count() == 1

    url = get_pull_up_counter_detail_url(bar2.id, counter.id)
    response = superuser_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert PullUpCounter.objects.count() == 1
