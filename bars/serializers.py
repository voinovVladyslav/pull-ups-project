from rest_framework import serializers

from tag.models import Tag
from tag.serializers import TagSerializer
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
    tags = TagSerializer(many=True)

    class Meta:
        model = Bars
        fields = [
            'id',
            'title',
            'latitude',
            'longitude',
            'address',
            'tags',
        ]
        read_only_fiels = ['id']

    def __init__(self, instance, data, **kwargs):
        super().__init__(instance, data, **kwargs)
        if hasattr(self, 'initial_data'):
            self.tags = self.initial_data.get('tags', [])
            if 'tags' in self.initial_data:
                self.initial_data['tags'] = []

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
        tags_data = validated_data.pop('tags')

        for tag_data in tags_data:
            Tag.objects.get_or_create(**tag_data)

        address = Address.objects.create(**address_data)
        bars = Bars.objects.create(address=address, **validated_data)
        return bars

    def update(self, instance, validated_data):
        address_data = validated_data.pop('address', {})
        new_tag_names = [tag_data['name'] for tag_data in self.tags]

        for key, value in address_data.items():
            setattr(instance.address, key, value)
        instance.address.save()

        for key, value in validated_data.items():
            if key == 'tags':
                continue
            setattr(instance, key, value)

        associated_tags = instance.tags.all()
        for tag in associated_tags:
            if tag.name not in new_tag_names:
                instance.tags.remove(tag)

        for tag in new_tag_names:
            obj, created = Tag.objects.get_or_create(name=tag)
            instance.tags.add(obj)

        instance.save()
        return instance
