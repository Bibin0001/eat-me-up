from django.urls import path, include
from .views import ShowShoppingList, EditShoppingList, CreateShoppingList, see_shopping_list, delete_shopping_list

urlpatterns = [
    path('', ShowShoppingList.as_view(), name='show shopping lists page'),
    path('create_shopping_list/', CreateShoppingList.as_view(), name='create shopping list page'),
    path('edit_shopping_list/<int:pk>', EditShoppingList.as_view(), name='edit shopping list page'),
    path('see_shopping_list/<int:pk>', see_shopping_list, name='show shopping list page'),
    path('delete_shopping_list/<int:pk>', delete_shopping_list, name='delete shopping list page')
]
