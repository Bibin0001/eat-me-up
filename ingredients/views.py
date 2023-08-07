from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView
from .models import Ingredient
from .form import IngredientForm
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.


class EditIngredient(UpdateView, LoginRequiredMixin):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredients/edit_ingredient.html'
    success_url = reverse_lazy('details ingredient page')

    def get_success_url(self):
        pk = self.kwargs['pk']

        return reverse_lazy('details ingredient page', kwargs={'pk': pk})

    def form_valid(self, form):
        ingredient = form.save(commit=False)
        ingredient.user = self.request.user
        ingredient.save()
        return super().form_valid(form)


class CreateIngredient(CreateView, LoginRequiredMixin):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredients/create_ingredient.html'
    success_url = reverse_lazy('index ingredients page')

    def form_valid(self, form):
        ingredient = form.save(commit=False)
        ingredient.user = self.request.user
        ingredient.save()
        return super().form_valid(form)


class ShowIngredients(ListView, LoginRequiredMixin):
    model = Ingredient
    template_name = 'ingredients/show_ingredients.html'
    context_object_name = 'ingredients'

    def get_queryset(self):
        return Ingredient.objects.filter(Q(user=self.request.user) | Q(user=None))


def ingredient_details(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)

    return render(request, 'ingredients/details_ingredient.html', context={'ingredient': ingredient})


def delete_ingredient(request, pk):
    ingredient = get_object_or_404(Ingredient, pk=pk)

    if ingredient.user == request.user:
        if request.method == 'POST':
            ingredient.delete()
            return redirect('show ingredients page')

        return render(request, 'ingredients/delete_ingredient.html', context={'ingredient': ingredient})


    else:
        return render(request, 'ingredients/cant_delete_ingredient.html', context={'ingredient': ingredient})
