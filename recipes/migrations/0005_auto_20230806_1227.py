# Generated by Django 3.2.12 on 2023-08-06 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0003_alter_ingredient_user'),
        ('recipes', '0004_savedrecipes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recipeingredient',
            name='ingredient',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ingredients.ingredient'),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='measurements',
            field=models.CharField(blank=True, choices=[('1', 'grams'), ('1000', 'kilograms')], max_length=21, null=True),
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='quantity',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]