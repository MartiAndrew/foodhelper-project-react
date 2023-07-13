from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from users.models import User
from recipes.models import Recipe, Favorites
from .serializers import FavoritesSerializer


class FavoritesView(APIView):
    """Класс представления для избранных рецептов,
    добавление и удаление"""

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, **kwargs):
        user = get_object_or_404(User, username=request.user)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))

        if request.method == 'POST':
            serializer = FavoritesSerializer(
                recipe, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            Favorites.objects.create(user=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        favor_recipe = get_object_or_404(
            Favorites, user=user, recipe=recipe
        )
        favor_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
