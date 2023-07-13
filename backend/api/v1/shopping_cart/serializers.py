from rest_framework import serializers, status

from recipes.models import ShoppingCart

from api.v1.recipe.serializers import RecipeSerializer


class ShoppingCartSerializer(RecipeSerializer):
    """Сериализатор добавления рецепта в корзину"""

    class Meta(RecipeSerializer.Meta):
        fields = ("id", "name", "image", "cooking_time")
        read_only_fields = ('name', 'cooking_time', 'image')

    def validate(self, data):
        recipe = self.instance
        user = self.context.get('request').user
        if ShoppingCart.objects.select_related('recipe', 'user').filter(
                recipe=recipe, user=user).exists():
            raise serializers.ValidationError(
                detail='Рецепт уже есть в корзине',
                code=status.HTTP_400_BAD_REQUEST,
            )
        return data
