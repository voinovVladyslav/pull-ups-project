import logging

from rest_framework import serializers

from .models import PullUpBars


logger = logging.getLogger('db')


class PullUpBarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PullUpBars
        fields = [
            'id',
        ]
        read_only_fiels = ['id']
