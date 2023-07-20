from django.urls import path, include
from .views import RegisterView, LoginUserView, account_details, log_out_user, account_creation,account_edit, change_user_macros

urlpatterns = [
    path('register', RegisterView.as_view(), name='register page'),
    path('login', LoginUserView.as_view(), name='login page'),
    path('account_details', account_details, name='account details page'),
    path('logout', log_out_user, name='log out page'),
    path('account_create', account_creation, name='account creation page'),
    path('account_edit', account_edit, name='account edit page'),
    path('account_macros_edit',change_user_macros , name='account macros edit page')
]
