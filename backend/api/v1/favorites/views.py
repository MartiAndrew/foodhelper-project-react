from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from recipes.models import Favorites, Recipe

from api.mixins import FavoriteShoppingMixin
from api.v1.favorites.serializers import FavoritesSerializer
from users.models import User


class FavoritesView(APIView, FavoriteShoppingMixin):
    """Класс представления для создания и удаления
    избранных рецептов"""
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, **kwargs):
        user = get_object_or_404(User, username=request.user)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))

        if request.method == 'POST':
            return self.perform_action(user, recipe, FavoritesSerializer, Favorites, request)
        elif request.method == 'DELETE':
            return self.delete_action(user, recipe, Favorites)
