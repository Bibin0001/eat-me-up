from django.contrib.auth.models import User
from django.db import models

from ingredients.models import Ingredient


# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=40)
    photo = models.ImageField(upload_to='recipe_photos', null=True, blank=True)

    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')

    instruction = models.TextField(max_length=300, null=True, blank=True)

    calories = models.FloatField(null=True, blank=True)
    proteins = models.FloatField(null=True, blank=True)
    carbs = models.FloatField(null=True, blank=True)
    fats = models.FloatField(null=True, blank=True)

    share = models.BooleanField(default=False)
    approved_for_sharing = models.BooleanField(default=False)
    def calculate_macros(self):
        calories = 0
        proteins = 0
        carbs = 0
        fats = 0

        for recipe_ingredient in self.recipeingredient_set.all():
            ingredient = recipe_ingredient.ingredient
            quantity = recipe_ingredient.quantity
            measurements = recipe_ingredient.measurements

            if measurements == 'kilograms':
                quantity = quantity * 1000

            calories += ingredient.calories_per_gram * quantity
            proteins += ingredient.proteins_per_gram * quantity
            carbs += ingredient.carbs_per_gram * quantity
            fats += ingredient.fats_per_gram * quantity

        self.calories = calories
        self.proteins = proteins
        self.carbs = carbs
        self.fats = fats

        self.save()

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        permissions = [
            ('approve_recipe', 'Can approve recipes for sharing')
        ]

    def save(self, *args, **kwargs):

        self.calculate_macros()
        super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.title}"


class RecipeIngredient(models.Model):
    MEASURING_TYPES = [
        ('1', 'grams'),
        ('1000', 'kilograms')
    ]

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    measurements = models.CharField(max_length=21, choices=MEASURING_TYPES)

class SavedRecipes(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f"Recipe: {self.recipe.title}"