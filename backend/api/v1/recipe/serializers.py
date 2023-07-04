from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from recipes.models import Recipe, AmountRecipe

class SubscriptionsRecipeSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для Recipe c укороченным набором полей
    для отображения в профиле пользователя."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = "__all__"

class AmountRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для связанной модели AmountRecipe"""
    id = serializers.IntegerField(source='Ingredient.id')
    name = serializers.ReadOnlyField(source='Ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='Ingredient.measurement_unit ')

    class Meta:
        model = AmountRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')

