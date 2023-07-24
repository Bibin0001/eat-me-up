from django.urls import path, include
from .views import index, create_recipe , edit_recipe, ShowRecipes

urlpatterns = [
    path('', index, name='recipes index page'),
    path('create_recipe', create_recipe, name='create recipe page'),
    path('show_recipes', ShowRecipes.as_view(), name='show recipes page'),
    path('edit_recipe/<int:pk>', edit_recipe, name='edit recipe page')
]
