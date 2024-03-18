from rest_framework.serializers import ModelSerializer

from .models import DipStation


class DipStationSerializer(ModelSerializer):
    class Meta:
        model = DipStation
        fields = [
            'id',
            'title',
        ]
        read_only_fields = ['id']
