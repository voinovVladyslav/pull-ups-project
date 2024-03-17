from django.contrib.gis.geos import Point
from rest_framework import status
from rest_framework.test import APIClient
from model_bakery.baker import make

from training_ground.models import TrainingGround
from training_ground.serializers import TrainingGroundSerializer
from .urls import TG_LIST_URL


def test_filter_does_not_apply_if_data_incorrect(db, api_client: APIClient):
    make(TrainingGround, 3)
    default_response = api_client.get(TG_LIST_URL)
    url = TG_LIST_URL + '?ref_point=20.20.43'
    filter_response = api_client.get(url)
    assert filter_response.status_code == status.HTTP_200_OK
    assert filter_response.content == default_response.content


def test_filter_works_correctly(db, api_client: APIClient):
    point1 = Point((30, 30), srid=4326)
    point2 = Point((20, 20), srid=4326)
    point3 = Point((80, 80), srid=4326)

    bars1 = make(TrainingGround, location=point1)
    bars2 = make(TrainingGround, location=point2)
    bars3 = make(TrainingGround, location=point3)

    url = TG_LIST_URL + '?ref_point=20.120;20.43'
    default_response = api_client.get(TG_LIST_URL)
    filter_response = api_client.get(url)
    assert filter_response.status_code == status.HTTP_200_OK
    assert filter_response.content != default_response.content
    data = filter_response.json()['results']
    assert data[0] == TrainingGroundSerializer(bars2).data
    assert data[1] == TrainingGroundSerializer(bars1).data
    assert data[2] == TrainingGroundSerializer(bars3).data
