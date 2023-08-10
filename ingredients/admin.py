from django.contrib import admin
from .models import Ingredient


# Register your models here.
@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'ingredient_type']
    search_fields = ['name', 'ingredient_type']

    list_filter = ['name', 'ingredient_type']
