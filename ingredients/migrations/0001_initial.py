# Generated by Django 4.2.3 on 2023-07-21 13:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('calories_per_gram', models.FloatField()),
                ('proteins_per_gram', models.FloatField()),
                ('carbs_per_gram', models.FloatField()),
                ('fats_per_gram', models.FloatField()),
                ('ingredient_type', models.CharField(choices=[('FRUITS', 'FRUITS'), ('PROTEIN', 'PROTEIN'), ('VEGETABLES', 'VEGETABLES'), ('DAIRY', 'DAIRY'), ('GRAINS', 'GRAINS')], max_length=30)),
                ('share', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
