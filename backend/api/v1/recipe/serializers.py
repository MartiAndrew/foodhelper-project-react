from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from recipes.models import Recipe

class SubscriptionsRecipeSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для Recipe c укороченным набором полей
    для отображения в профиле пользователя."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = "__all__"
