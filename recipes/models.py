from django.contrib.auth.models import User
from django.db import models


class Ingredient(models.Model):
    name = models.CharField(max_length=100)
    calories_per_gram = models.FloatField()
    proteins_per_gram = models.FloatField()
    carbs_per_gram = models.FloatField()
    fats_per_gram = models.FloatField()

    def __str__(self):
        return f"{self.name}"


# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=40)
    photo = models.ImageField(upload_to='recipe_photos', null=True, blank=True)

    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')

    instruction = models.TextField(max_length=300, null=True, blank=True)

    calories = models.FloatField()
    proteins = models.FloatField()
    carbs = models.FloatField()
    fats = models.FloatField()

    def calculate_macros(self):
        calories = 0
        proteins = 0
        carbs = 0
        fats = 0

        for recipe_ingredient in self.ingredients.all():
            ingredient = recipe_ingredient.ingredient

            quantity = recipe_ingredient.quantity
            measuring_type = recipe_ingredient.measuring_type

            if measuring_type == 'kilograms':
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

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"


class RecipeIngredient(models.Model):
    MEASURING_TYPES = [
        ('grams', 'grams'),
        ('kilograms', 'kilograms')
    ]

    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    measurements = models.CharField(max_length=20, choices=MEASURING_TYPES)
