# Generated by Django 4.2.3 on 2023-07-27 23:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ingredients', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ingredient',
            name='share',
        ),
    ]
