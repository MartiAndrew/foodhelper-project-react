from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

User = get_user_model()


class Tag(models.Model):
    """Класс описывающий модель тэгов у рецепта"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название тэга',
        unique=True
    )
    color = models.CharField(
        max_length=7,
        verbose_name='Цветовой HEX-код',
        default='#FF0000',
        validators=[
            RegexValidator(
                regex=r'^#[A-Fa-f0-9]{6}$',
                message='Цвет должен быть в формате HEX-кода (#RRGGBB).'
            )
        ]
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Слаг тэга',
        unique=True,
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Класс описывающий модель ингредиента"""
    name = models.CharField(
        max_length=200,
        verbose_name='Название ингредиента',
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения'
    )

    class Meta:
        ordering = ('id',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f'{self.name}({self.measurement_unit})'


class Recipe(models.Model):
    """Класс описывающий модель рецепта"""
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes',
    )
    name = models.CharField(
        max_length=200,
        verbose_name='Название рецепта'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/',
    )
    text = models.TextField(
        verbose_name='Описание блюда')
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='RecipeIngredient',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Теги')
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(
            MinValueValidator(
                1, message='Минимальное время приготовления - 1 минута.'),
        )
    )

    class Meta:
        ordering = ('-id',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    """Класс описывающий промежуточную модель
    между моделями Ингридиента и Рецепта, в которой
    обозначается количество ингредиентов в рецепте.
    """
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=(
            MinValueValidator(
                1, message='Мин. количество ингридиента 1'),),
        verbose_name='количество ингредиента'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipeingredients')
    ingredient = models.ForeignKey(
        'Ingredient',
        on_delete=models.CASCADE,
        related_name='ingredient')

    class Meta:
        verbose_name = 'Количество ингредиента'
        verbose_name_plural = 'Количество ингредиентов'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['recipe', 'ingredient'],
                name='unique ingredient')]


class Favorites(models.Model):
    """
    Класс описывающий модель избранных рецептов у пользователя
    """
    user = models.ForeignKey(
        User,
        verbose_name='Пользователь',
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
    )
    recipe = models.ForeignKey(
        Recipe,
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
        related_name='favorite_recipe'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite')]

    def __str__(self):
        return f'{self.user}, {self.recipe.name}'




class ShoppingCart(models.Model):
    """
    Класс описывающий модель корзины покупок рецептов пользователя.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь')
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Покупка')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name="unique_recipe"
            )
        ]

    def __str__(self):
        return f'{self.user}, {self.recipe.name}'


