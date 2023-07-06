from rest_framework import status, viewsets

from recipes.models import Recipe
from users.permissions import IsAuthorOrReadOnly
from .serializers import RecipeSerializer, RecipeCreateSerializer


class RecipeViewSet(viewsets.ModelViewSet):
    """Класс представления для рецепта."""
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = IsAuthorOrReadOnly
    ordering = ('-id',)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PUT', 'PATCH']:
            return RecipeCreateSerializer
        return RecipeSerializer






