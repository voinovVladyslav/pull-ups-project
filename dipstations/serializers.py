from rest_framework.serializers import ModelSerializer

from .models import DipStations


class DipStationSerializer(ModelSerializer):
    class Meta:
        model = DipStations
        fields = [
            'id',
            'title',
        ]
        read_only_fields = ['id']
