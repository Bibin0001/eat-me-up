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

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2 input-color'

        self.fields['breakfast'].widget.attrs['class'] += 'form-select'
        self.fields['lunch'].widget.attrs['class'] += 'form-select'
        self.fields['dinner'].widget.attrs['class'] += 'form-select'
