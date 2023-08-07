from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Account


class CreateUser(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = [
            'email', 'username', 'password1', 'password2'
        ]


class AccountCreation(forms.ModelForm):
    class Meta:
        model = Account

        fields = ['weight', 'height', 'age', 'gender', 'goal', 'activity']
        exclude = ['calories', 'protein', 'carbs', 'fats', 'user', ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2 input-color'

        self.fields['gender'].widget.attrs['class'] = 'select-style form-control mb-2 input-color'
        self.fields['goal'].widget.attrs['class'] = 'select-style form-control mb-2 input-color'
        self.fields['activity'].widget.attrs['class'] = 'select-style form-control mb-2 input-color'


class AccountChangeMacros(forms.ModelForm):
    class Meta:
        model = Account

        fields = ['calories', 'protein', 'carbs', 'fats', ]
        exclude = ['weight', 'height', 'age', 'gender', 'goal', 'activity', 'user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control mb-2 input-color'
