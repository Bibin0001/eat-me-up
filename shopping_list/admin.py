from django.contrib import admin
from .models import ShoppingList



@admin.register(ShoppingList)
class ShoppingListAdmin(admin.ModelAdmin):
    list_display = ['title']
    search_fields = ['title', 'recipes__title']
    list_filter = ['title']
