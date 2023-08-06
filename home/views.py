from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from datetime import date
from accounts.views import check_if_user_has_completed_the_profile
from .models import UserSelectedPlan
from .form import UserSelectPlanForm
from eating_plan.models import EatingPlan


# Create your views here.
def index(request):
    user = request.user
    if user.is_authenticated:
        account = check_if_user_has_completed_the_profile(user)

        if not account:
            return redirect('account creation page')

        try:
            user_selected_plan = UserSelectedPlan.objects.get(user=request.user, selected_date=date.today())
        except UserSelectedPlan.DoesNotExist:
            user_selected_plan = None

        context = {
            "user": request.user,
            'account': account,
            'plan': user_selected_plan

        }

        return render(request, 'home/index.html', context=context)
    return render(request, 'home/index.html', context={"user": request.user})


@login_required
def change_eating_plan(request, pk):
    eating_plan = get_object_or_404(UserSelectedPlan, pk=pk)

    if request.method == 'POST':
        form = UserSelectPlanForm(request.POST, user=request.user, instance=eating_plan)
        if form.is_valid():
            form.save()

            return redirect('home page')


    else:
        form = UserSelectPlanForm(user=request.user, instance=eating_plan)

    context = {
        'form': form
    }

    return render(request, 'home/edit_plan_for_the_day.html', context=context)


@login_required
def create_eating_plan_for_the_day(request):
    user_plans = EatingPlan.objects.filter(user=request.user)
    if not user_plans:
        return redirect('create eating plan page')

    if request.method == 'POST':
        form = UserSelectPlanForm(request.POST, user=request.user)
        if form.is_valid():
            plan_for_the_day = form.save(commit=False)

            plan_for_the_day.user = request.user
            plan_for_the_day.save()

            return redirect('home page')


    else:
        form = UserSelectPlanForm(user=request.user)

    context = {
        'form': form
    }

    return render(request, 'home/select_plan_for_the_day.html', context=context)


def delete_plan_for_the_day(request, pk):
    plan_for_the_day = get_object_or_404(UserSelectedPlan, pk=pk)

    if request.method == 'POST':
        plan_for_the_day.delete()
        return redirect('home page')

    return render(request, 'home/delete_plan_for_the_day.html')
