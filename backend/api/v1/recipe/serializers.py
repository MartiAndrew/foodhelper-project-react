from rest_framework import serializers

from drf_extra_fields.fields import Base64ImageField

from recipes.models import Recipe, Ingredient, AmountRecipe, Tag
from ..users.serializers import CustomUserSerializer
from ..tags.serializers import TagSerializer


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
    tags = serializers.PrimaryKeyRelatedField(many=True,
                                              queryset=Tag.objects.all(),
                                              required=True)
    ingredients = AmountRecipeSerializer(many=True)
    image = Base64ImageField(required=True)

    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ('author',)

    def validate_ingredients(self, value):
        if not all(ingredient['amount'] for ingredient in value):
            raise serializers.ValidationError(
                'Количество ингредиента не должно быть равно нулю'
            )
        return value

    def create_ingredients(self, ingredients, recipe):
        AmountRecipe.objects.bulk_create([AmountRecipe(
            recipe=recipe,
            ingredient_id=ingredient['ingredient']['id'],
            amount=ingredient.get('amount')) for ingredient in ingredients
        ])

    def create(self, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        recipe = Recipe.objects.create(**validated_data)
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        if 'ingredients' in validated_data:
            ingredients = validated_data.pop('ingredients')
            instance.ingredients.clear()
            self.create_ingredients(ingredients, instance)
        if 'tags' in validated_data:
            instance.tags.set(
                validated_data.pop('tags'))
        return super().update(
            instance, validated_data)

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeSerializer(instance, context=context).data
