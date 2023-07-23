from django import forms
from .models import Recipe, RecipeIngredient, Ingredient


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'photo', 'instruction']

        exclude = ['user', 'share']

    def __init__(self, *args, **kwargs):
        super(RecipeForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class RecipeIngredientForm(forms.ModelForm):
    ingredient = forms.ModelChoiceField(queryset=Ingredient.objects.all())

    class Meta:
        model = RecipeIngredient
        fields = ['ingredient', 'quantity', 'measurements']

        widgets = {
            'quantity': forms.NumberInput(attrs={'dataChange': 'updateRecipeMacros'})
        }

    def __init__(self, *args, **kwargs):
        super(RecipeIngredientForm, self).__init__(*args, **kwargs)

        # Set the 'name' attribute for the ingredient field's widget
        self.fields['ingredient'].widget.attrs['name'] = 'nameee'
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

        self.fields['ingredient'].widget.attrs['class'] = 'ingredients'
        self.fields['ingredient'].widget.attrs['dataChange'] = 'updateRecipeMacros'
        self.fields['measurements'].widget.attrs['dataChange'] = 'updateRecipeMacros'
        # self.fields['ingredient'].widget.attrs['style'] = 'display:none'
        # self.fields['quantity'].widget.attrs['style'] = 'display:none'
        # self.fields['measurements'].widget.attrs['style'] = 'display:none'
