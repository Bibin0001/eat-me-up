from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Ingredient(models.Model):
    INGREDIENT_TYPES = [
        ("FRUITS", "FRUITS"),
        ("PROTEIN", "PROTEIN"),
        ("VEGETABLES", "VEGETABLES"),
        ("DAIRY", "DAIRY"),
        ("GRAINS", "GRAINS")]

    name = models.CharField(max_length=100)
    calories_per_gram = models.FloatField()
    proteins_per_gram = models.FloatField()
    carbs_per_gram = models.FloatField()
    fats_per_gram = models.FloatField()

    ingredient_type = models.CharField(max_length=30, choices=INGREDIENT_TYPES)
    share = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"
