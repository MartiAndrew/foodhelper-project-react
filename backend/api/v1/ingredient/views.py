from rest_framework import viewsets

from .serializers import IngredientSerializer
from recipes.models import Ingredient
from users.permissions import IsAdminOrReadOnly
from ...filters import IngredientSearchFilter


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Класс представления для ингредиента."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
