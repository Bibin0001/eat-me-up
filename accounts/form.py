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


class AccountChangeMacros(forms.ModelForm):
    class Meta:
        model = Account

        fields = ['calories', 'protein', 'carbs', 'fats', ]
        exclude = ['weight', 'height', 'age', 'gender', 'goal', 'activity', 'user']

