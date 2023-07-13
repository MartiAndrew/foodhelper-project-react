from rest_framework import viewsets

from recipes.models import Tag

from users.permissions import IsAdminOrReadOnly

from .serializers import TagSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """Класс представления для тэга."""
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = None
