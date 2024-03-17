from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer
from rest_framework_gis.fields import GeometryField

from .models import TrainingGround


class TrainingGroundSerializer(GeoModelSerializer):
    location = GeometryField()
    is_favorite = serializers.BooleanField(required=False, read_only=True)

    class Meta:
        model = TrainingGround
        geo_field = 'location'
        fields = [
            'id',
            'is_favorite',
            'location',
            'pullupbar',
        ]
        read_only_fields = [
            'id',
        ]

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
