from rest_framework import viewsets

from recipes.models import Ingredient

from api.filters import IngredientSearchFilter
from users.permissions import IsAdminOrReadOnly

from .serializers import IngredientSerializer


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Класс представления для ингредиента."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
    filter_backends = (IngredientSearchFilter,)
    search_fields = ('^name',)
