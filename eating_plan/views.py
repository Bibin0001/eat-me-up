from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from recipes.models import Recipe
from .models import EatingPlan
from .form import EatingPlanForm


# Create your views here.
@login_required
def delete_eating_plan(request, pk):
    plan = get_object_or_404(EatingPlan, pk=pk)

    if request.method == 'POST':
        plan.delete()

        return redirect('show eating plans page')
    context = {
        'plan': plan
    }

    return render(request, 'eating_plan/delete_eating_plan.html', context=context)


@login_required
def show_eating_plan_details(request, pk):
    plan = get_object_or_404(EatingPlan, pk=pk)

    context = {
        'plan': plan
    }

    return render(request, 'eating_plan/details_eating_plan.html', context=context)


@login_required
def edit_eating_plan(request, pk):
    plan = get_object_or_404(EatingPlan, pk=pk)

    if request.method == 'POST':
        form = EatingPlanForm(request.user, request.POST, instance=plan)
        if form.is_valid():
            eating_plan = form.save(commit=False)
            eating_plan.user = request.user
            eating_plan.save()

            return redirect('show eating plans page')

    else:
        form = EatingPlanForm(request.user, instance=plan)

    context = {
        'form': form,
        'plan': plan,
        'recipes': Recipe.objects.all()
    }

    return render(request, 'eating_plan/edit_eating_plan.html', context=context)


class ShowEatingPlans(ListView, LoginRequiredMixin):
    model = EatingPlan
    template_name = 'eating_plan/index.html'
    context_object_name = 'eating_plans'

    def get_queryset(self):
        return EatingPlan.objects.filter(user=self.request.user)


class CreateEatingPlan(CreateView, LoginRequiredMixin):
    model = EatingPlan
    form_class = EatingPlanForm
    template_name = 'eating_plan/create_eating_plan.html'
    success_url = reverse_lazy('show eating plans page')

    def form_valid(self, form):
        eating_plan = form.save(commit=False)
        eating_plan.user = self.request.user

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['recipes'] = Recipe.objects.filter(user=self.request.user)
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
