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

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        address = Address.objects.create(**address_data)
        bars = Bars.objects.create(address=address, **validated_data)
        return bars

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', {})

        for key, value in address_data.items():
            setattr(instance.address, key, value)
        instance.address.save()

        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()

        return instance
