from django import forms
from .models import UserSelectedPlan
from eating_plan.models import EatingPlan


class UserSelectPlanForm(forms.ModelForm):
    plan = forms.ModelChoiceField(queryset=EatingPlan.objects.none())

    class Meta:
        model = UserSelectedPlan
        fields = ['plan']
        exclude = ['selected_date', 'user']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

        self.fields['plan'].queryset = EatingPlan.objects.filter(user=user)
