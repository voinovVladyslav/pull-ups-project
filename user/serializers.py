from rest_framework import serializers

from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

from achievements.helpers.upsert import upsert_achievements
from achievements.helpers.check.query import (
    get_total_different_bars_used_today,
    get_current_pullup_streak,
    get_max_pullups,
    get_total_bars,
    get_total_pullups
)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'password', 'is_staff']
        extra_kwargs = {
            'password': {'write_only': True, 'min_length': 8},
            'is_staff': {'read_only': True},
        }

    def create(self, validated_data):
        user = get_user_model().objects.create_user(**validated_data)
        upsert_achievements(user)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user


class UserStatisticsSerializer(serializers.ModelSerializer):
    total_pullups = serializers.SerializerMethodField()
    max_pullups = serializers.SerializerMethodField()
    bars_visited = serializers.SerializerMethodField()
    bars_visited_today = serializers.SerializerMethodField()
    current_streak = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = [
            'total_pullups',
            'max_pullups',
            'bars_visited',
            'bars_visited_today',
            'current_streak',
        ]
        read_only_fields = [
            'total_pullups',
            'max_pullups',
            'bars_visited',
            'bars_visited_today',
            'current_streak',
        ]

    def get_total_pullups(self, obj):
        return get_total_pullups(obj)

    def get_max_pullups(self, obj):
        return get_max_pullups(obj)

    def get_bars_visited(self, obj):
        return get_total_bars(obj)

    def get_bars_visited_today(self, obj):
        return get_total_different_bars_used_today(obj)

    def get_current_streak(self, obj):
        return get_current_pullup_streak(obj)


class TokenSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request=self.context.get('request'),
            email=email,
            password=password,
        )
        if not user:
            msg = _('Unable to authenticate with provided credentials')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
