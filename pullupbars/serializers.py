import logging

from django.forms.models import model_to_dict
from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer
from rest_framework_gis.fields import GeometryField

from .models import PullUpBars


logger = logging.getLogger('db')


class BarsSerializer(GeoModelSerializer):
    location = GeometryField()
    is_favorite = serializers.BooleanField(required=False, read_only=True)

    class Meta:
        model = PullUpBars
        geo_field = 'location'
        fields = [
            'id',
            'title',
            'location',
            'is_favorite',
        ]
        read_only_fiels = ['id']

    def validate_location(self, value):
        # x - longitude y - latitude
        if value.x <= -180 or value.x >= 180:
            raise serializers.ValidationError(
                'Longitude shoud be in range from -180 to 180'
            )
        if value.y <= -90 or value.y >= 90:
            raise serializers.ValidationError(
                'Latitude shoud be in range from -90 to 90'
            )
        return value

    def create(self, validated_data):
        bars = PullUpBars.objects.create(**validated_data)
        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        logger.info(
            'Created bars: %s',
            model_to_dict(bars),
            extra=dict(type='bars_create', pullupbar=bars, user=user)
        )
        return bars
