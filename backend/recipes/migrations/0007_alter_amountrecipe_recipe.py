# Generated by Django 3.2 on 2023-07-09 18:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_auto_20230709_1547'),
    ]

    operations = [
        migrations.AlterField(
            model_name='amountrecipe',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe', to='recipes.recipe'),
        ),
    ]