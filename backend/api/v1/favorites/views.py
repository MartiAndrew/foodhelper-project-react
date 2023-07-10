from rest_framework import generics, status
from rest_framework.response import Response

from ..recipe.mixins import GetObjectMixin



class FavoriteCreateDel(GetObjectMixin,
                        generics.RetrieveDestroyAPIView,
                        generics.ListCreateAPIView):
    """Класс представления для избранных рецептов,
    добавление и удаление"""

    def create(self, request, *args, **kwargs):
        instance = self.get_object()
        request.user.favorite_recipe.recipe.add(instance)
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def perform_destroy(self, instance):
        self.request.user.favorite_recipe.recipe.remove(instance)
