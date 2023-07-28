from django.contrib.auth.models import User
from django.db import models

from recipes.models import Recipe


# Create your models here.
class ShoppingList(models.Model):
    title = models.CharField(max_length=30)
    recipes = models.ManyToManyField(Recipe)

    additional_info = models.TextField(max_length=200, null=True, blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
