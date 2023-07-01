from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

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
        verbose_name='Цвет тэга',
        unique=True,
        db_index=False,
    )
    slug = models.SlugField(
        max_length=200,
        verbose_name='Слаг тэга',
        unique=True,
        db_index=False,
    )

    class Meta:
        ordering = ('name',)
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
        ordering = ('name',)
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name


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
        verbose_name='Название'
    )
    image = models.ImageField(
        verbose_name='Изображение',
        upload_to='recipes/images/',
    )
    text = models.TextField(
        verbose_name='Описание блюда')
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        through='recipes.AmountRecipe',
    )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Теги')
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )
    cooking_time = models.PositiveSmallIntegerField(
        'Время приготовления',
        validators=(
            MinValueValidator(
                1, message='Минимальное время приготовления - 1 минута.'),
        )
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class AmountRecipe(models.Model):
    """Класс описывающий промежуточную модель
    между моделями Ингридиента и Рецепта, в которой
    обозначается количество ингредиентов в рецепте.
    """
    amount = models.PositiveSmallIntegerField(
        default=1,
        validators=(
            MinValueValidator(
                1, message='Мин. количество ингридиентов 1'),),
        verbose_name='количество ингредиентов'

    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe')
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

    def __str__(self):
        return (
            f'Рецепт: {self.recipe}, Ингредиент: {self.ingredient}, '
            f'Количество: {self.amount}')


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

    def __str__(self):
        return f'Пользователь: {self.user}, Рецепт: {self.recipe}'


class ShoppingCart(models.Model):
    """
    Класс описывающий модель корзины покупок рецептов пользователя.
    """
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        null=True,
        verbose_name='Пользователь')
    recipe = models.ManyToManyField(
        Recipe,
        related_name='shopping_cart',
        verbose_name='Покупка')

    class Meta:
        ordering = ['-id']
        verbose_name = 'Покупка'
        verbose_name_plural = 'Покупки'

    def __str__(self):
        recipe_list = ", ".join([item.name for item in self.recipe.all()])
        user_info = str(self.user) if self.user else "Пользователь не задан"
        return f'Пользователь: {user_info}. Покупка: {recipe_list}.'
