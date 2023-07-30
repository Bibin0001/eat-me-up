from django import forms

from recipes.models import Recipe
from .models import EatingPlan


class EatingPlanForm(forms.ModelForm):
    class Meta:
        model = EatingPlan
        fields = ['title', 'breakfast', 'lunch', 'dinner']


    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['breakfast'].queryset = Recipe.objects.filter(user=user)
        self.fields['lunch'].queryset = Recipe.objects.filter(user=user)
        self.fields['dinner'].queryset = Recipe.objects.filter(user=user)
