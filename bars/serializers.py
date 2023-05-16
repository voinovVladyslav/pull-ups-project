from rest_framework import serializers
from .models import Address, Bars


class AddresSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            'country',
            'city',
            'street',
            'number',
            'postal_code',
        ]


class BarsSerializer(serializers.ModelSerializer):
    address = AddresSerializer(required=True, read_only=False)

    class Meta:
        model = Bars
        fields = [
            'id',
            'title',
            'latitude',
            'longitude',
            'address',
        ]
        read_only_fiels = ['id']

    def validate_latitude(self, value):
        if value < -90 or value > 90:
            raise serializers.ValidationError(
                "Latitude must be between -90 and 90."
            )
        return value

    def validate_longitude(self, value):
        if value < -180 or value > 180:
            raise serializers.ValidationError(
                "Longitude must be between -180 and 180."
            )
        return value
