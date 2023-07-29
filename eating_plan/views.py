from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from recipes.models import Recipe
from .models import EatingPlan
from .form import EatingPlanForm


# Create your views here.

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
        context['recipes'] = Recipe.objects.all()
        return context
