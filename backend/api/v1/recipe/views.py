from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend

from recipes.models import Recipe
from .serializers import RecipeSerializer, RecipeCreateSerializer
from ..shopping_cart.views import ShoppingCartGetView
from ...filters import CustomRecipeFilter


class RecipeViewSet(ShoppingCartGetView,
                    viewsets.ModelViewSet):
    """Класс представления для рецепта."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = CustomRecipeFilter
    http_method_names = ['get', 'post', 'patch', 'delete']
    ordering = ('-id',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return RecipeCreateSerializer
        return RecipeSerializer
