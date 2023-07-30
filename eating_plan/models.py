from django.contrib.auth.models import User
from django.db import models

from recipes.models import Recipe


# Create your models here.
class EatingPlan(models.Model):
    title = models.CharField(max_length=40)

    breakfast = models.ForeignKey(Recipe, related_name='breakfast_plan', on_delete=models.SET_NULL, null=True)
    lunch = models.ForeignKey(Recipe, related_name='lunch_plan', on_delete=models.SET_NULL, null=True)
    dinner = models.ForeignKey(Recipe, related_name='dinner_plan', on_delete=models.SET_NULL, null=True)

    total_calories = models.FloatField(null=True, blank=True)
    total_proteins = models.FloatField(null=True, blank=True)
    total_carbs = models.FloatField(null=True, blank=True)
    total_fats = models.FloatField(null=True, blank=True)

    def calculate_macros(self):
        self.total_calories = (
                self.breakfast.calories + self.lunch.calories + self.dinner.calories
        )
        self.total_proteins = (
                self.breakfast.proteins + self.lunch.proteins + self.dinner.proteins
        )
        self.total_carbs = (
                self.breakfast.carbs + self.lunch.carbs + self.dinner.carbs
        )
        self.total_fats = (
                self.breakfast.fats + self.lunch.fats + self.dinner.fats
        )

    def save(self, *args, **kwargs):
        self.calculate_macros()
        super().save(*args, **kwargs)

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"
