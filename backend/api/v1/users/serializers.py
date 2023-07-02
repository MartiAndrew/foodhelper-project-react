from rest_framework import serializers
from djoser.serializers import UserCreateSerializer, UserSerializer
import django.contrib.auth.password_validation as validators

from users.models import CustomUser, Subscribe


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания модели CustomUser"""

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')

    def validate_password(self, password):
        validators.validate_password(password)
        return password


class CustomUserSerializer(UserSerializer):
    """Сериализатор для использования с моделью СustomUser."""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name',
                  'last_name', 'is_subscribed',)

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous:
            return False
        return user.following.filter(author=obj).exists()

