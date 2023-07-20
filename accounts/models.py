from django.db import models

# Create your models here.
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


# Create your models here.
class Account(models.Model):
    GENDER_CHOICES = [
        ('Male', 'Male'),
        ('Female', 'Female')
    ]

    GOALS_CHOICES = [
        ('Lose Weight', 'Lose Weight'),
        ('Gain Weight', 'Gain Weight'),
        ('Maintain Weight', 'Maintain Weight')
    ]

    ACTIVITY_LEVEL_CHOICES = [
        ('Sedentary', 'Sedentary'),
        ('Lightly Active', 'Lightly Active'),
        ('Moderately Active', 'Moderately Active'),
        ('Very Active', 'Very Active'),
        ('Extra Active', 'Extra Active')
    ]

    weight = models.IntegerField()
    height = models.IntegerField()
    age = models.IntegerField(validators=[MinValueValidator(5)])
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    goal = models.CharField(max_length=30, choices=GOALS_CHOICES)
    activity = models.CharField(max_length=30, choices=ACTIVITY_LEVEL_CHOICES)

    calories = models.IntegerField(validators=[MinValueValidator(100)])
    protein = models.IntegerField(validators=[MinValueValidator(0)])
    carbs = models.IntegerField(validators=[MinValueValidator(0)])
    fats = models.IntegerField(validators=[MinValueValidator(0)])

    user = models.OneToOneField(User, on_delete=models.CASCADE)
