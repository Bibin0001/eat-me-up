from django import forms
from .models import EatingPlan


class EatingPlanForm(forms.ModelForm):
    class Meta:
        model = EatingPlan
        fields = ['title', 'breakfast', 'lunch', 'dinner']
