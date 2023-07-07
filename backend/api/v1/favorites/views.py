from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from ..recipe.mixins import FavoriteShoppingMixin
from users.models import CustomUser
from recipes.models import Recipe, Favorites
from .serializers import FavoriteSerializer


class FavoriteView(APIView, FavoriteShoppingMixin):
    """Класс представления для избранных рецептов,
    с наследованием от кастомного миксина."""

    @action(detail=True,
            methods=['post', 'delete'],
            permission_classes=[IsAuthenticated], )
    def favorite(self, request, **kwargs):
        user = get_object_or_404(CustomUser, username=request.user)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))

        if request.method == 'POST':
            return self.perform_action(
                user, recipe, FavoriteSerializer, Favorites)
        elif request.method == 'DELETE':
            return self.delete_action(user, recipe, Favorites)
