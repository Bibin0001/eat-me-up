from django.urls import path, include
from .views import home, create_ingredient

urlpatterns = [
    path('', home, name='index ingredients page'),
    path('create/', create_ingredient, name='create ingredient page')
]
