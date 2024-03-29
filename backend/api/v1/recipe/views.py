from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter

from api.filters import RecipeFilter
from api.pagination import Pagination
from api.v1.favorites.views import FavoritesView
from api.v1.recipe.serializers import RecipeCreateSerializer, RecipeSerializer
from api.v1.shopping_cart.views import ShoppingCartView
from recipes.models import Recipe
from users.permissions import IsAuthorOrReadOnly


class RecipeViewSet(ShoppingCartView,
                    FavoritesView,
                    viewsets.ModelViewSet):
    """Класс представления для рецепта."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = Pagination
    permission_classes = (IsAuthorOrReadOnly,)
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filterset_class = RecipeFilter
    ordering = ('-id',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return RecipeCreateSerializer
        return RecipeSerializer
