from django.core.paginator import Paginator
import django.contrib.auth.password_validation as validators
from djoser.serializers import UserCreateSerializer, UserSerializer
from email_validator import validate_email, EmailNotValidError
from rest_framework import serializers, status
from rest_framework.serializers import ValidationError

from recipes.models import Recipe
from users.models import CustomUser, Subscribe

PAGE_SIZE = 3


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
        request = self.context.get('request', )
        if not request or request.user.is_anonymous:
            return False
        return Subscribe.author.filter(user=request.user,
                                       author=obj).exists()


class SubscriptionsRecipeSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для Recipe c укороченным набором полей
    для отображения в профиле пользователя."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(serializers.ModelSerializer):
    """Сериализатор вывода авторов, на которых подписан
    текущий пользователь."""
    email = serializers.ReadOnlyField(source='user.email')
    id = serializers.ReadOnlyField(source='author.id')
    username = serializers.ReadOnlyField(source='author.username')
    first_name = serializers.ReadOnlyField(source='author.first_name')
    last_name = serializers.ReadOnlyField(source='author.last_name')
    is_subscribed = serializers.SerializerMethodField('get_is_subscribed')
    recipes = serializers.SerializerMethodField('get_recipes')
    recipes_count = serializers.SerializerMethodField('get_recipes_count')

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed', 'recipes', 'recipes_count',)

    def get_recipes_count(self, obj):
        return obj.recipes.count()

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.following.filter(user=user, author=obj.id).exists()

    def get_recipes(self, obj):
        recipes = Recipe.objects.filter(author=obj.following)
        paginator = Paginator(recipes, PAGE_SIZE)
        recipes_paginated = paginator.page(1)
        serializer = SubscriptionsRecipeSerializer(recipes_paginated, many=True)
        return serializer.data

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
