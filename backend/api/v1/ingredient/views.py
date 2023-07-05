from rest_framework import viewsets

from .serializers import IngredientSerializer
from recipes.models import Ingredient


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """Класс представления для ингредиента."""
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
