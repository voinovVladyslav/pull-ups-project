from rest_framework import status
from rest_framework.test import APIClient
from model_bakery.baker import make

from training_ground.models import TrainingGround
from user.models import User
from .urls import (
    TG_LIST_URL,
    get_training_ground_add_favorite_url,
    get_training_ground_remove_favorite_url,
)


def test_list_all_favorite_training_grounds(
    db, superuser_client: APIClient, superuser_email
):
    training_grounds = make(TrainingGround, 5)
    user = User.objects.get(email=superuser_email)
    user.favorite_training_grounds.add(training_grounds[0])
    user.favorite_training_grounds.add(training_grounds[1])

    url = TG_LIST_URL + '?is_favorite=true'
    response = superuser_client.get(url)
    response_data = response.json()['results']
    assert response.status_code == status.HTTP_200_OK
    assert len(response_data) == 2
    for tg_data in response_data:
        assert tg_data['is_favorite'] is True
        assert tg_data['id'] in [
            training_grounds[0].id, training_grounds[1].id
        ]


def test_add_favorite_training_ground(
    db, superuser_client: APIClient, superuser_email
):
    training_ground = make(TrainingGround)
    user = User.objects.get(email=superuser_email)
    assert user.favorite_training_grounds.count() == 0

    url = get_training_ground_add_favorite_url(training_ground.id)
    response = superuser_client.post(url)
    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    assert user.favorite_training_grounds.count() == 1


def test_remove_favorite_training_ground(
    db, superuser_client: APIClient, superuser_email
):
    training_ground = make(TrainingGround)
    user = User.objects.get(email=superuser_email)
    user.favorite_training_grounds.add(training_ground)
    assert user.favorite_training_grounds.count() == 1

    url = get_training_ground_remove_favorite_url(training_ground.id)
    response = superuser_client.post(url)
    assert response.status_code == status.HTTP_200_OK

    user.refresh_from_db()
    assert user.favorite_training_grounds.count() == 0
