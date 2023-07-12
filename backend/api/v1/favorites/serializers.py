from rest_framework import serializers, status

from api.v1.recipe.serializers import RecipeSerializer
from recipes.models import Favorites, Recipe



class FavoritRecipeSerializer(RecipeSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'cooking_time', 'image')
        read_only_fields = ('name', 'cooking_time', 'image')

    def validate(self, data):
        recipe = self.instance
        user = self.context.get('request').user
        if Favorites.objects.filter(recipe=recipe, user=user).exists():
            raise serializers.ValidationError(
                detail='Рецепт уже в избранных',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data
