from rest_framework.views import APIView
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.formats import date_format
from rest_framework import status
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from api.v1.shopping_cart.serializers import ShoppingCartSerializer
from users.models import User
from recipes.models import RecipeIngredient, ShoppingCart, Recipe


class ShoppingCartView(APIView):
    """Класс представления для создания, удаления и
    скачивания корзины покупок"""

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, **kwargs):
        """Метод для создания им удаления списка покупок."""
        user = get_object_or_404(User, username=request.user)
        recipe = get_object_or_404(Recipe, id=self.kwargs.get('pk'))

        if request.method == 'POST':
            serializer = ShoppingCartSerializer(
                recipe, data=request.data, context={'request': request})
            serializer.is_valid(raise_exception=True)
            ShoppingCart.objects.create(user=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        cart_recipe = get_object_or_404(
            ShoppingCart, user=user, recipe=recipe
        )
        cart_recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Метод для скачивания списка покупок."""
        user = request.user
        if not user.shopping_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)

        ingredients = (
            RecipeIngredient.objects.filter(
                recipe__shopping_cart__user=user
            )
            .values(
                'ingredient__name',
                'ingredient__measurement_unit',
            )
            .annotate(sum_amount=Sum('amount')).order_by()
        )

        today = date_format(timezone.now(), use_l10n=True)
        headline = (
            f'Дата: {today} \n\n'
            f'Список покупок: \n\n'
        )
        lines = []
        for ingredient in ingredients:
            line = (
                f'➤ {ingredient["ingredient__name"]} '
                f'({ingredient["ingredient__measurement_unit"]})'
                f' -- {ingredient["sum_amount"]}'
            )
            lines.append(line)

        shopping_list = headline + '\n'.join(lines)
        filename = 'shopping_list.txt'
        response = HttpResponse(shopping_list, content_type='text/plain')
        response['Content-Disposition'] = f'attachment; filename={filename}'
        return response
