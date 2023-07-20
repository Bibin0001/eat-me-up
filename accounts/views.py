from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .form import CreateUser, AccountCreation, AccountChangeMacros
from django.contrib.auth.views import LoginView
from .macros_calculator import Macros
from .models import Account
from django.contrib.auth.decorators import login_required


@login_required
def change_user_macros(request):
    account = request.user.account
    if request.method == 'POST':
        form = AccountChangeMacros(request.POST, instance=account)

        if form.is_valid():
            account.calories = form.cleaned_data['calories']
            account.protein = form.cleaned_data['protein']
            account.carbs = form.cleaned_data['carbs']
            account.fats = form.cleaned_data['fats']

            account.save()

            return redirect('account details page')
    else:
        form = AccountChangeMacros(instance=account)

    return render(request, 'accounts/accout_update_macros.html', context={'form': form})


# Create your views here.

class RegisterView(CreateView):
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('account creation page')
    form_class = CreateUser

    def form_valid(self, form):
        response = super().form_valid(form)
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user)

        return response


class LoginUserView(LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True

    # success_url = reverse_lazy("account creation page")

    def get_success_url(self):
        return reverse_lazy('home page')


@login_required
def account_details(request):
    account = check_if_user_has_completed_the_profile(request.user)
    if not account:
        return redirect('account creation page')
    else:

        return render(request, 'accounts/account_details.html', context={'account': account})


def check_if_user_has_completed_the_profile(user):
    try:
        account = user.account
        return account
    except Account.DoesNotExist:
        return False


@login_required
def account_creation(request):
    if request.method == 'POST':
        form = AccountCreation(request.POST)

        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            goal = form.cleaned_data['goal']
            activity_level = form.cleaned_data['activity']
            user_macros = Macros(weight, height, age, gender, goal, activity_level)

            user_profile = Account(
                weight=weight,
                height=height,
                age=age,
                gender=gender,
                goal=goal,
                activity=activity_level,
                calories=user_macros.calories,
                protein=user_macros.proteins,
                carbs=user_macros.carbs,
                fats=user_macros.fats,
                user=request.user
            )

            user_profile.save()

            return redirect('account details page')
    else:
        form = AccountCreation()

    context = {'form': form}

    return render(request, 'accounts/account_create.html', context=context)


@login_required
def account_edit(request):
    account = request.user.account
    if request.method == 'POST':
        form = AccountCreation(request.POST, instance=account)

        if form.is_valid():
            weight = form.cleaned_data['weight']
            height = form.cleaned_data['height']
            age = form.cleaned_data['age']
            gender = form.cleaned_data['gender']
            goal = form.cleaned_data['goal']
            activity_level = form.cleaned_data['activity']
            user_macros = Macros(weight, height, age, gender, goal, activity_level)

            account.weight = weight
            account.height = height
            account.age = age
            account.gender = gender
            account.goal = goal
            account.activity = activity_level
            account.calories = user_macros.calories
            account.protein = user_macros.proteins
            account.carbs = user_macros.carbs
            account.fats = user_macros.fats

            account.save()

            return redirect('account details page')
    else:
        form = AccountCreation(instance=account)

    return render(request, 'accounts/account_edit.html', context={'form': form})


@login_required
def log_out_user(request):
    if request.method == "POST":
        logout(request)
        return redirect('home page')

    return render(request, 'accounts/log_out.html')
