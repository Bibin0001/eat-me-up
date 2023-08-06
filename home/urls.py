from django.urls import path, include
from .views import index, create_eating_plan_for_the_day, change_eating_plan, delete_plan_for_the_day

urlpatterns = [
    path('', index, name='home page'),
    path('select_plan_for_the_day', create_eating_plan_for_the_day, name='select eating plan for the day page'),
    path('change_plan_for_the_day/<int:pk>', change_eating_plan, name='change eating plan for the day page'),
    path('delete_plan_for_the_day/<int:pk>',delete_plan_for_the_day, name='delete eating plan for the day page'),
]
