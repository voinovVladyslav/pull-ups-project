from rest_framework.serializers import ModelSerializer

from .models import PullUpCounter, DipCounter


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


class DipCounterSerializer(ModelSerializer):
    class Meta:
        model = DipCounter
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
