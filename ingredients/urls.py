from django.urls import path, include
from .views import ShowIngredients, CreateIngredient, EditIngredient, ingredient_details, delete_ingredient

urlpatterns = [
    path('create/', CreateIngredient.as_view(), name='create ingredient page'),
    path('show_ingredients', ShowIngredients.as_view(), name='show ingredients page'),
    path('edit_ingredient/<int:pk>', EditIngredient.as_view(), name='edit ingredient page'),
    path('details_ingredient/<int:pk>', ingredient_details, name='details ingredient page'),
    path('delete_ingredient/<int:pk>', delete_ingredient, name='delete ingredient page')
]
