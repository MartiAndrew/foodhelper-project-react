from rest_framework import viewsets

from recipes.models import Recipe
from api.v1.users.permissions import IsAdminOrAuthorOrReadOnly
from .serializers import RecipeSerializer, RecipeCreateSerializer
from api.v1.favorites.views import FavoriteView
from api.v1.shopping_cart.views import ShoppingCartView

class RecipeViewSet(FavoriteView,
                    ShoppingCartView,
                    viewsets.ModelViewSet):
    """Класс представления для рецепта."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = (IsAdminOrAuthorOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    ordering = ('-id',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return RecipeCreateSerializer
        return RecipeSerializer
