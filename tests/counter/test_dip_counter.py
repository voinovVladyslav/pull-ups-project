from rest_framework import status
from model_bakery.baker import make

from counter.models import DipCounter
from dipstations.models import DipStations
from user.models import User
from .urls import get_dip_counter_detail_url, get_dip_counter_list_url


def test_authentication_required(
    db, api_client, create_user
):
    dip = make(DipStations)
    user = create_user()
    make(DipCounter, dipstation=dip, user=user)

    url = get_dip_counter_list_url(dip.id)
    response = api_client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED


def test_return_only_user_related_counter(
    db, superuser_client, superuser_email, create_user
):
    dip = make(DipStations)
    user = User.objects.get(email=superuser_email)
    second_user = create_user()
    make(DipCounter, 5, user=user, dipstation=dip)
    make(DipCounter, 5, user=second_user, dipstation=dip)
    assert DipCounter.objects.count() == 10

    url = get_dip_counter_list_url(dip.id)
    response = superuser_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    response_counters = response.data
    assert len(response_counters) + 1 == 5


def test_create_counter(db, superuser_client, superuser_email):
    dip = make(DipStations)
    user = User.objects.get(email=superuser_email)
    payload = {
        'reps': 10,
    }
    assert DipCounter.objects.count() == 0
    url = get_dip_counter_list_url(dip.id)
    response = superuser_client.post(url, payload)
    assert response.status_code == status.HTTP_201_CREATED
    assert DipCounter.objects.count() == 1
    counter = DipCounter.objects.first()
    assert counter.reps == payload['reps']
    assert counter.user == user
    assert counter.dipstation == dip


def test_create_counter_invalid_dip_id(db, superuser_client):
    dip = make(DipStations)
    payload = {
        'reps': 10,
    }
    url = get_dip_counter_list_url(dip.id + 1)
    response = superuser_client.post(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert DipCounter.objects.count() == 0


def test_update_counter(db, superuser_client, superuser_email):
    user = User.objects.get(email=superuser_email)
    counter = make(DipCounter, user=user)
    url = get_dip_counter_detail_url(counter.dipstation.id, counter.id)
    payload = {
        'reps': 20,
    }
    response = superuser_client.patch(url, payload)
    assert response.status_code == status.HTTP_200_OK
    counter.refresh_from_db()
    assert counter.reps == payload['reps']


def test_update_counter_invalid_payload(db, superuser_client, superuser_email):
    dipstation = make(DipStations)
    user = User.objects.get(email=superuser_email)
    reps = 10
    counter = make(DipCounter, user=user, reps=reps, dipstation=dipstation)
    payload = {
        'reps': -20,
    }
    url = get_dip_counter_detail_url(dipstation.id, counter.id)
    response = superuser_client.patch(url, payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    counter.refresh_from_db()
    assert counter.reps == reps


def test_delete_counter(db, superuser_client, superuser_email):
    user = User.objects.get(email=superuser_email)
    counter = make(DipCounter, user=user)
    assert DipCounter.objects.count() == 1

    url = get_dip_counter_detail_url(counter.dipstation.id, counter.id)
    response = superuser_client.delete(url)
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert DipCounter.objects.count() == 0


def test_delete_counter_using_differend_dipstation_id_error(
    db, superuser_client, superuser_email
):
    user = User.objects.get(email=superuser_email)
    counter = make(DipCounter, user=user)
    other_dipstation = make(DipStations)
    assert DipCounter.objects.count() == 1

    url = get_dip_counter_detail_url(other_dipstation.id, counter.id)
    response = superuser_client.delete(url)
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert DipCounter.objects.count() == 1
