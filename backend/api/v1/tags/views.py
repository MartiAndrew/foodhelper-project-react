from rest_framework import viewsets

from .serializers import TagSerializer
from recipes.models import Tag
from users.permissions import IsAdminOrReadOnly


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Класс представления для тэга."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None

