from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers, status

from recipes.models import Recipe
from users.models import Subscribe, User


class CustomUserCreateSerializer(UserCreateSerializer):
    """Сериализатор для создания модели CustomUser."""

    class Meta(UserCreateSerializer.Meta):
        model = User
        fields = ('email', 'id', 'username',
                  'first_name', 'last_name', 'password')


class CustomUserSerializer(UserSerializer):
    """Cериализатор просмотра профиля пользователя"""
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'last_name',
                  'is_subscribed',)
        read_only_fields = ("is_subscribed",)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        return user.follower.filter(author=obj).exists()


class SubscriptionsRecipeSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для Recipe c укороченным набором полей
    для отображения в профиле пользователя."""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class SubscribeSerializer(UserSerializer):
    """Сериализатор вывода авторов, на которых подписан
    текущий пользователь."""
    is_subscribed = serializers.SerializerMethodField()
    recipes = serializers.SerializerMethodField()
    recipes_count = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = (
            'id', 'email', 'username', 'first_name', 'last_name',
            'is_subscribed', 'recipes', 'recipes_count',
        )
        read_only_fields = ('email', 'username', 'first_name', 'last_name')

    def get_recipes_count(self, obj):
        """Метод указывает кол-во рецептов пользователя"""
        return obj.recipes.count()

    def get_is_subscribed(self, obj):
        """Метод проверяет подписку на пользователя."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.follower.filter(author=obj).exists()

    def get_recipes(self, obj):
        """Метод показывает рецепты пользователя."""
        request = self.context.get('request')
        recipes_limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        if recipes_limit:
            recipes = recipes[: int(recipes_limit)]
        serializer = SubscriptionsRecipeSerializer(recipes,
                                                   many=True, read_only=True)
        return serializer.data

    def validate(self, data):
        author = self.instance
        user = self.context.get('request').user
        if Subscribe.objects.filter(author=author, user=user).exists():
            raise serializers.ValidationError(
                detail='Подписка на этого пользователя уже есть',
                code=status.HTTP_400_BAD_REQUEST,
            )
        if user == author:
            raise serializers.ValidationError(
                detail='Нельзя подписаться на самого себя',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data
