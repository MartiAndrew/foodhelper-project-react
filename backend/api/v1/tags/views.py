from rest_framework import viewsets

from .serializers import TagSerializer
from recipes.models import Tag

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
