import webcolors
from rest_framework import serializers


class Hex2NameColor(serializers.Field):
    """
    Добавление цвета при создании тега
    #ffff00 - желтый
    #00ff00 - зеленый
    #ff0000 - красный
    """

    def to_representation(self, value):
        return value

    def to_internal_value(self, data):
        try:
            webcolors.hex_to_name(data)
        except ValueError:
            raise serializers.ValidationError("Для этого цвета нет имени")
        return data