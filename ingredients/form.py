from django import forms
from .models import Ingredient


class IngredientForm(forms.ModelForm):
    class Meta:
        model = Ingredient
        fields = ['name', 'calories_per_gram', 'proteins_per_gram', 'carbs_per_gram', 'fats_per_gram', 'ingredient_type']
        exclude = ['user', 'share']

    def __init__(self, *args, **kwargs):
        super(IngredientForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2 input-color'
