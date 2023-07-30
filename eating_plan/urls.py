from django.urls import path, include
from .views import ShowEatingPlans, CreateEatingPlan, edit_eating_plan, show_eating_plan_details, delete_eating_plan

urlpatterns = [
    path('', ShowEatingPlans.as_view(), name='show eating plans page'),
    path('create_eating_plan/',CreateEatingPlan.as_view(), name='create eating plan page' ),
    path('edit_eating_plan/<int:pk>', edit_eating_plan, name='edit eating plan page'),
    path('show_eating_plan_details/<int:pk>', show_eating_plan_details, name='show eating plans details page'),
    path('delete_eating_plan/<int:pk>', delete_eating_plan, name='delete eating plan page')
]