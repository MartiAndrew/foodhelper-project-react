from rest_framework import serializers, status

from recipes.models import Recipe, Favorites
from ..recipe.serializers import RecipeSerializer


class FavoriteSerializer(RecipeSerializer):
    """Сериализатор для избранных рецептов"""

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('name', 'image', 'cooking_time')

    def validate(self, data):
        recipe = self.instance
        user = self.context.get('request').user
        if Favorites.objects.filter(recipe_id=recipe.pk, user=user).exists():
            raise serializers.ValidationError(
                detail='Рецепт уже в избранном',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data
