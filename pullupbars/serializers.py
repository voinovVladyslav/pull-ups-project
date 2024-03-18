from rest_framework import serializers

from .models import PullUpBars


class PullUpBarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PullUpBars
        fields = [
            'id',
            'title',
        ]
        read_only_fiels = ['id']
