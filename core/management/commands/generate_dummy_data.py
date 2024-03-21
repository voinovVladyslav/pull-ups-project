import json
import random

from django.core.management.base import BaseCommand
from django.contrib.gis.geos import Point
from training_ground.models import TrainingGround
from pullupbars.models import PullUpBars
from dipstations.models import DipStations
from pull_up_project.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Generate dummy data for testing'

    def handle(self, *args, **options):
        TrainingGround.objects.all().delete()
        DipStations.objects.all().delete()
        PullUpBars.objects.all().delete()

        path = BASE_DIR / 'core' / 'management' / 'commands' / 'cities.json'
        with open(path, 'r') as f:
            cities = json.load(f)

        for city in cities:
            base_lat = float(city['lat'])
            base_lon = float(city['lng'])
            for _ in range(random.randint(25, 75)):
                point = Point(
                    base_lon + random.uniform(-0.05, 0.05),
                    base_lat + random.uniform(-0.05, 0.05)
                )
                pullupbar = None
                dipstation = None
                value = random.uniform(0, 1)
                if value < 0.95:
                    pullupbar = PullUpBars.objects.create()
                if value > 0.05:
                    dipstation = DipStations.objects.create()

                assert pullupbar or dipstation

                TrainingGround.objects.create(
                    location=point,
                    pullupbar=pullupbar,
                    dipstation=dipstation
                )
