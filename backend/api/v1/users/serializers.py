from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
import django.contrib.auth.password_validation as validators
from email_validator import validate_email, EmailNotValidError
from rest_framework import serializers
from rest_framework.serializers import ValidationError

from users.models import CustomUser
from recipes.models import Recipe


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания модели CustomUser."""

    class Meta(UserCreateSerializer.Meta):
        model = CustomUser
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')

    def validate_email(self, data):
        try:
            validate_email(data)
        except EmailNotValidError:
            raise ValidationError("Неверный формат адреса эл. почты.")

        if CustomUser.objects.filter(email=data).exists():
            raise ValidationError("Пользователь с таким адресом эл. почты уже существует.")

        return data

    def validate_password(self, password):
        validators.validate_password(password)
        return password

    def validate_username(self, data):
        if CustomUser.objects.filter(username=data).exists():
            raise ValidationError(
                "Пользователь с таким никнеймом уже существует."
            )
        return data


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


class SubscriptionsRecipeSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для Recipe c укороченным набором полей."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = "__all__"


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор вывода авторов, на которых подписан текущий пользователь."""
    is_subscribed = serializers.SerializerMethodField()
    recipes = SubscriptionsRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count',)

    def get_is_subscribed(self, obj):
        return True

    def get_recipes_count(self, obj):
        return obj.recipes.count()
