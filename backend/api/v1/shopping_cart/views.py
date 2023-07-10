from django.db.models import Sum
from django.http import HttpResponse
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from recipes.models import AmountRecipe
from .pdf_generate import pdf_generate
from ..recipe.mixins import GetObjectMixin


class ShoppingCartCreateDel(GetObjectMixin,
                            generics.RetrieveDestroyAPIView,
                            generics.ListCreateAPIView):
    """Класс представления для корзины покупок,
    добавление и удаление рецепта из корзины."""

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        request.user.shopping_cart.recipe.add(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        self.request.user.shopping_cart.recipe.remove(instance)


class ShoppingCartGetView(APIView):
    """Класс представления для скачивания корзины покупок"""

    @action(detail=False,
            methods=['GET'],
            permission_classes=(IsAuthenticated,)
            )
    def download_shopping_cart(self, request):
        """Метод получения и выгрузки в PDF-file списка покупок."""
        if not request.user.shopping_cart.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredients = (
            AmountRecipe.objects.filter(
                recipe__shopping_cart__user=request.user
            )
            .prefetch_related('ingredient')
            .values(
                'ingredient__name',
                'ingredient__measurement_unit',
            )
            .annotate(sum_amount=Sum('amount')).order_by()
        )
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment;'
        text_cart = ''
        for value in ingredients:
            text_cart += ' '.join([
                value['ingredient__name'],
                '-',
                str(value['amount__sum']),
                value['ingredient__measurement_unit'],
                '<br/>'
            ])
        return pdf_generate(text_cart, response)
