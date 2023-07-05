from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from recipes.models import Recipe, AmountRecipe
from ..users.serializers import CustomUserSerializer
from ..tags.serializers import TagSerializer


class SubscriptionsRecipeSerializer(serializers.ModelSerializer):
    """Базовый сериализатор для Recipe c укороченным набором полей
    для отображения в профиле пользователя."""
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = "__all__"


class AmountRecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для связанной модели AmountRecipe."""
    id = serializers.IntegerField(source='Ingredient.id')
    name = serializers.ReadOnlyField(source='Ingredient.name')
    measurement_unit = serializers.ReadOnlyField(source='Ingredient.measurement_unit ')

    class Meta:
        model = AmountRecipe
        fields = ('id', 'name', 'measurement_unit', 'amount')


class RecipeSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения модели Recipe."""
    author = CustomUserSerializer()
    ingredients = AmountRecipeSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField(read_only=True)
    is_in_shopping_cart = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')

    def get_is_favorited(self, obj) -> bool:
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.favorite_recipe.filter(recipe=obj).exists()

    def get_is_in_shopping_cart(self, obj) -> bool:
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return user.shopping_cart.filter(recipe=obj).exists()


class RecipeCreateSerializer(serializers.ModelSerializer):
    """Сериализатор описывающий поля для создания рецепта."""
    pass
