from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import FormView, CreateView
from .models import Ingredient
from .form import IngredientForm


# Create your views here.
def home(request):
    return render(request, 'ingredients/index.html')


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
