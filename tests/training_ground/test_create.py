from rest_framework import status

from training_ground.models import TrainingGround
from dipstations.models import DipStations
from pullupbars.models import PullUpBars
from .urls import TG_LIST_URL


def test_create_training_ground(db, superuser_client, superuser_email):
    payload = {
        'location': {
            'type': 'Point',
            'coordinates': [12.9721, 77.5933],
        }
    }

    response = superuser_client.post(TG_LIST_URL, payload, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert TrainingGround.objects.count() == 1
    tg = TrainingGround.objects.first()
    dipstation = DipStations.objects.first()
    assert dipstation
    pullupbar = PullUpBars.objects.first()
    assert pullupbar
    assert tg.dipstation == dipstation
    assert tg.pullupbar == pullupbar
