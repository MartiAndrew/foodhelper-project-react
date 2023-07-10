from django.shortcuts import get_object_or_404
from rest_framework.permissions import AllowAny

from api.v1.users.serializers import SubscriptionsRecipeSerializer
from recipes.models import Recipe


class GetObjectMixin:
    """Миксина для удаления/добавления рецептов избранных/корзины."""

    serializer_class = SubscriptionsRecipeSerializer
    permission_classes = (AllowAny,)

    def get_object(self):
        recipe_id = self.kwargs['recipe_id']
        recipe = get_object_or_404(Recipe, id=recipe_id)
        self.check_object_permissions(self.request, recipe)
        return recipe

