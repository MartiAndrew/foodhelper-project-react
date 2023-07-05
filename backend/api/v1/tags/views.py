from rest_framework import viewsets

from .serializers import TagSerializer
from recipes.models import Tag

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Класс представления для тэга."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
