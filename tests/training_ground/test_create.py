from rest_framework import status

from training_ground.models import TrainingGround
from dipstations.models import DipStations
from pullupbars.models import PullUpBars
from .urls import TG_LIST_URL


def test_create_training_ground(db, superuser_client):
    payload = {
        'location': {
            'type': 'Point',
            'coordinates': [12.9721, 77.5933],
        },
        'create_pullupbar': False,
        'create_dipstation': False,
    }

    response = superuser_client.post(TG_LIST_URL, payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert TrainingGround.objects.count() == 1
    assert DipStations.objects.count() == 0
    assert PullUpBars.objects.count() == 0
    tg = TrainingGround.objects.first()
    assert tg.dipstation is None
    assert tg.pullupbar is None


def test_create_with_pullupbar_only(db, superuser_client):
    payload = {
        'location': {
            'type': 'Point',
            'coordinates': [12.9721, 77.5933],
        },
        'create_pullupbar': True,
        'create_dipstation': False,
    }

    response = superuser_client.post(TG_LIST_URL, payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert TrainingGround.objects.count() == 1
    assert DipStations.objects.count() == 0
    assert PullUpBars.objects.count() == 1
    tg = TrainingGround.objects.first()
    assert tg.dipstation is None
    assert tg.pullupbar == PullUpBars.objects.first()


def test_create_with_dipstation_only(db, superuser_client):
    payload = {
        'location': {
            'type': 'Point',
            'coordinates': [12.9721, 77.5933],
        },
        'create_dipstation': True,
        'create_pullupbar': False,
    }

    response = superuser_client.post(TG_LIST_URL, payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert TrainingGround.objects.count() == 1
    assert DipStations.objects.count() == 1
    assert PullUpBars.objects.count() == 0
    tg = TrainingGround.objects.first()
    assert tg.dipstation == DipStations.objects.first()
    assert tg.pullupbar is None


def test_create_with_dipstation_and_pullupbar(db, superuser_client):
    payload = {
        'location': {
            'type': 'Point',
            'coordinates': [12.9721, 77.5933],
        },
        'create_pullupbar': True,
        'create_dipstation': True,
    }

    response = superuser_client.post(TG_LIST_URL, payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert TrainingGround.objects.count() == 1
    assert DipStations.objects.count() == 1
    assert PullUpBars.objects.count() == 1
    tg = TrainingGround.objects.first()
    assert tg.dipstation == DipStations.objects.first()
    assert tg.pullupbar == PullUpBars.objects.first()
