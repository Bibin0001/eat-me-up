from django.urls import path, include
from .views import index, create_recipe, edit_recipe, ShowUserRecipes, recipe_details, delete_recipe, \
    ShowPendingRecipes, \
    approve_recipe, ShowSharedRecipes, shared_recipe_details

urlpatterns = [
    path('', index, name='recipes index page'),
    path('create_recipe', create_recipe, name='create recipe page'),
    path('show_recipes', ShowUserRecipes.as_view(), name='show recipes page'),
    path('edit_recipe/<int:pk>', edit_recipe, name='edit recipe page'),
    path('details_recipe/<int:pk>', recipe_details, name='details recipe page'),
    path('delete_recipe/<int:pk>', delete_recipe, name='delete recipe page'),
    path('show_pending_recipes/', include([
        path('', ShowPendingRecipes.as_view(), name='show pending recipes page'),
        path('approve_recipe/<int:pk>', approve_recipe, name='approve pending recipe page')
    ])),
    path('shared_recipes', include([
        path('', ShowSharedRecipes.as_view(), name='show shared recipes page'),
        path('shared_recipe_details/<int:pk>', shared_recipe_details, name='details shared recipe page')
    ]))

]
