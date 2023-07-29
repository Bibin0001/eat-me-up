from django.urls import path, include
from .views import ShowEatingPlans, CreateEatingPlan
urlpatterns = [
    path('', ShowEatingPlans.as_view(), name='show eating plans page'),
    path('create_eating_plan/',CreateEatingPlan.as_view(), name='create eating plan page' )
]