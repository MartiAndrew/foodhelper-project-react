from rest_framework import serializers

from .fields import Hex2NameColor
from recipes.models import Tag


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер для просмотра тегов."""
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = '__all__'
