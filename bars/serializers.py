import logging

from django.forms.models import model_to_dict
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework_gis.serializers import GeoModelSerializer
from rest_framework_gis.fields import GeometryField

from tag.models import Tag
from tag.serializers import TagSerializer
from .models import Bars


logger = logging.getLogger('db')


class BarsSerializer(GeoModelSerializer):
    tags = TagSerializer(many=True, required=False)
    location = GeometryField()
    is_favorite = serializers.BooleanField(required=False, read_only=True)

    class Meta:
        model = Bars
        geo_field = 'location'
        fields = [
            'id',
            'title',
            'location',
            'tags',
            'is_favorite',
        ]
        read_only_fiels = ['id']

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        if hasattr(self, 'initial_data'):
            self.tags = self.initial_data.pop('tags', [])

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
        bars = Bars.objects.create(**validated_data)
        for tag_data in self.tags:
            tag = Tag.objects.get_or_create(**tag_data)
            bars.tags.add(tag)

        user = None
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            user = request.user

        logger.info(
            'Created bars: %s',
            model_to_dict(bars),
            extra=dict(type='bars_create', bar=bars, user=user)
        )
        return bars

    def update(self, instance, validated_data):
        new_tag_names = [tag_data['name'] for tag_data in self.tags]

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
