import django.contrib.auth.password_validation as validators
from email_validator import validate_email, EmailNotValidError
from rest_framework import serializers, status
from rest_framework.serializers import ValidationError

from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField

from users.models import CustomUser, Subscribe
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
    """Cериализатор просмотра профиля пользователя"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed',)
        read_only_fields = ("is_subscribed",)

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        if user.is_anonymous or (user == obj):
            return False
        return user.follower.filter(author=obj).exists()


class SubscriptionsRecipeSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для Recipe c укороченным набором полей
    для отображения в профиле пользователя."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор вывода авторов, на которых подписан текущий пользователь."""
    is_subscribed = serializers.BooleanField(read_only=True, default=True)
    recipes = SubscriptionsRecipeSerializer(many=True, read_only=True)
    recipes_count = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('email', 'id', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count',)

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if Subscribe.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError(
                detail='Подписка уже существует',
                code=status.HTTP_400_BAD_REQUEST,
            )
        if user == author:
            raise serializers.ValidationError(
                detail='Подписка на самого себя невозможна',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data
