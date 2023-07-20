from django.urls import path, include
from .views import index, create_recipe, RecipeCreateView

urlpatterns = [
    path('', index, name='recipes index page'),
    path('create_recipe', create_recipe, name='create recipe page')
]