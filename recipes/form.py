from django import forms
from django.db.models import Q
from django.forms import BaseFormSet, BaseModelFormSet

from .models import Recipe, RecipeIngredient, Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title',  'instruction', 'share']

        exclude = ['user', 'approved_for_sharing', 'photo']

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2 input-color'



class RecipeIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.none())

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'measurements']

        widgets = {
            'quantity': forms.NumberInput(attrs={'dataChange': 'updateRecipeMacros'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(RecipeIngredientForm, self).__init__(*args, **kwargs)
        self.fields['ingredient'].queryset = Ingredient.objects.filter(
            Q(user=user) | Q(user=None)
        )
        # Set the 'name' attribute for the ingredient field's widget
        self.fields['ingredient'].widget.attrs['name'] = 'nameee'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2 input-color'


        self.fields['ingredient'].widget.attrs['class'] += 'ingredients form-select input-color'
        self.fields['ingredient'].widget.attrs['dataChange'] = 'updateRecipeMacros'
        self.fields['measurements'].widget.attrs['dataChange'] = 'updateRecipeMacros'



class RecipeIngredientFormUserSetUp(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def _construct_form(self, i, **kwargs):
        kwargs['user'] = self.user
        return super()._construct_form(i, **kwargs)