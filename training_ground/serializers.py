from rest_framework import serializers
from rest_framework_gis.serializers import GeoModelSerializer
from rest_framework_gis.fields import GeometryField

from pullupbars.models import PullUpBars
from dipstations.models import DipStations
from .models import TrainingGround


class TrainingGroundSerializer(GeoModelSerializer):
    location = GeometryField()
    is_favorite = serializers.BooleanField(required=False, read_only=True)
    create_pullupbar = serializers.BooleanField(
        write_only=True, required=True
    )
    create_dipstation = serializers.BooleanField(
        write_only=True, required=True
    )

    class Meta:
        model = TrainingGround
        geo_field = 'location'
        fields = [
            'id',
            'is_favorite',
            'location',
            'pullupbar',
            'dipstation',
            'create_pullupbar',
            'create_dipstation',
        ]
        read_only_fields = [
            'id',
            'pullupbar',
            'dipstation',
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

    def create(self, validated_data):
        create_pullupbar = validated_data.pop('create_pullupbar')
        create_dipstation = validated_data.pop('create_dipstation')
        tg: TrainingGround = super().create(validated_data)

        if create_pullupbar:
            tg.pullupbar = PullUpBars.objects.create()

        if create_dipstation:
            tg.dipstation = DipStations.objects.create()

        tg.save()
        return tg
