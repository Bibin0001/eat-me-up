from django.urls import path, include
from .views import home, create_ingredient, ShowIngredients, CreateIngredient, EditIngredient

urlpatterns = [
    path('', home, name='index ingredients page'),
    path('create/', CreateIngredient.as_view(), name='create ingredient page'),
    path('show_ingredients', ShowIngredients.as_view(), name='show ingredients page'),
    path('edit_ingredient/<int:pk>', EditIngredient.as_view(), name ='edit ingredient page')
]
