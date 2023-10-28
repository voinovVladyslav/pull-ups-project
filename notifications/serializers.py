from rest_framework import serializers

from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = [
            'id',
            'message',
            'unread',
            'redirect_to',
            'created_at',
        ]
        read_only_fields = [
            'id',
            'message',
            'redirect_to',
            'created_at',
        ]
