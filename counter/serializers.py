from rest_framework.serializers import ModelSerializer

from .models import PullUpCounter


class PullUpCounterSerializer(ModelSerializer):
    class Meta:
        model = PullUpCounter
        fields = [
            'id',
            'reps',
            'created_at',
            'updated_at',
        ]
        read_only_fields = [
            'id',
            'created_at',
            'updated_at',
        ]
