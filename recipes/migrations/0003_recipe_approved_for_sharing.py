# Generated by Django 4.2.3 on 2023-07-27 11:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_alter_recipe_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='approved_for_sharing',
            field=models.BooleanField(default=False),
        ),
    ]
