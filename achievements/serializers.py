from rest_framework import serializers

from .models import Achievement


class AchievementSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Achievement
        fields = [
            'id',
            'title',
            'description',
            'done',
            'achieved_at',
            'image',
        ]
        read_only_fields = [
            'image'
        ]

    def get_image(self, obj) -> str | None:
        if obj.image:
            return obj.image.image_url
        return None
