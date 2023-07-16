from rest_framework import serializers

from recipes.models import Tag
from api.v1.tags.fields import Hex2NameColor


class TagSerializer(serializers.ModelSerializer):
    """Сериалайзер для просмотра тегов."""
    color = Hex2NameColor()

    class Meta:
        model = Tag
        fields = '__all__'
