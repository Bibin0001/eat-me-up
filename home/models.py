from django.contrib.auth.models import User
from django.db import models

from eating_plan.models import EatingPlan


# Create your models here.
class UserSelectedPlan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(EatingPlan, on_delete=models.CASCADE)
    selected_date = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.plan.title}"
