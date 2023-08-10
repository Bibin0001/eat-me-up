from django.contrib import admin
from .models import Recipe, RecipeIngredient


class RecipeIngredientInLine(admin.TabularInline):
    model = RecipeIngredient


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'share', 'approved_for_sharing']
    search_fields = ['title', 'share', 'approved_for_sharing']
    list_filter = ['approved_for_sharing', 'share']
    inlines = [RecipeIngredientInLine]

    actions = ['approve_for_sharing']

    def approve_for_sharing(self, queryset):
        queryset.update(approved_for_sharing=True)

    approve_for_sharing.short_description = 'Approve selected recipes for sharing'


@admin.register(RecipeIngredient)
class RecipeIngredientAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'ingredient', 'quantity', 'measurements']
    search_fields = ['recipe__title', 'ingredient__name', 'quantity', 'measurements']
    list_filter = ['recipe', 'ingredient']
    ordering = ['recipe']
