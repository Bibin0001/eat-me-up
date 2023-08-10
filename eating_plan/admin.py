from django.contrib import admin
from .models import EatingPlan


@admin.register(EatingPlan)
class EatingPlanAdmin(admin.ModelAdmin):
    list_display = ['title', 'breakfast', 'lunch', 'dinner']
    list_filter = ['title', 'breakfast', 'lunch', 'dinner']
    search_fields = ['title', 'breakfast__title', 'lunch__title', 'dinner__title']
# Register your models here.
