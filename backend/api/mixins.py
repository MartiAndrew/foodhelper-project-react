from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response


class FavoriteShoppingMixin:
    """Класс-миксин общий для представлений списка избранных
    рецептов и корзины покупок."""

    def perform_action(
            self, user, recipe, serializer_class, model_class, request):
        serializer = serializer_class(
            recipe, data=request.data, context={'request': request})
        if serializer.is_valid():
            model_class.objects.create(user=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.error, status=status.HTTP_400_BAD_REQUEST)

    def delete_action(self, user, recipe, model_class):
        favorite_recipe = get_object_or_404(
            model_class, user=user, recipe=recipe
        )
        favorite_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
