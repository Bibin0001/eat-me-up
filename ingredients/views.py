from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView
from .models import Ingredient
from .form import IngredientForm
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def home(request):
    return render(request, 'ingredients/index.html')


class EditIngredient(UpdateView, LoginRequiredMixin):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredients/edit_ingredient.html'
    success_url = reverse_lazy('index ingredients page')

    def form_valid(self, form):
        ingredient = form.save(commit=False)
        ingredient.user = self.request.user
        ingredient.save()
        return super().form_valid(form)


class CreateIngredient(CreateView, LoginRequiredMixin):
    model = Ingredient
    form_class = IngredientForm
    template_name = 'ingredients/create_ingredient.html'

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


def create_ingredient(request):
    if request.method == 'POST':
        form = IngredientForm(request.POST)

        if form.is_valid():
            ingredient = form.save(commit=False)

            ingredient.user = request.user

            ingredient.save()

            return redirect('index ingredients page')
    else:
        form = IngredientForm

    context = {
        'form': form
    }
    return render(request, 'ingredients/create_ingredient.html', context=context)
