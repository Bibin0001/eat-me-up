from django.contrib import admin
from .models import UserSelectedPlan


@admin.register(UserSelectedPlan)
class UserSelectedPlanAdmin(admin.ModelAdmin):
    list_display = ['plan', 'selected_date']
    search_fields = ['plan__title']
    list_filter = ['plan']

# Register your models here.
