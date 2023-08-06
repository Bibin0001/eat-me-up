from django import forms

from .models import ShoppingList
from recipes.models import Recipe


class ShoppingListForm(forms.ModelForm):
    recipes = forms.ModelMultipleChoiceField(
        queryset=None
    )

    class Meta:
        model = ShoppingList
        fields = ['title', 'recipes', 'additional_info']
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(ShoppingListForm, self).__init__(*args, **kwargs)

        self.fields['recipes'].queryset = Recipe.objects.filter(user=user)


        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2 input-color'

