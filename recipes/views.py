from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.forms import formset_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.forms.models import modelformset_factory
from .form import RecipeForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient
from ingredients.models import Ingredient
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def index(request):
    return render(request, 'recipes/index.html')


class ShowRecipes(ListView, LoginRequiredMixin):
    model = Recipe
    template_name = 'recipes/show_recipes.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.filter(user=self.request.user)


@login_required
def create_recipe(request):
    RecipeIngredientFormSet = formset_factory(RecipeIngredientForm, extra=30)

    if request.method == 'POST':
        form = RecipeForm(request.POST)
        formset = RecipeIngredientFormSet(request.POST)

        if form.is_valid() and formset.is_valid():

            recipe = form.save(commit=False)

            recipe.user = request.user
            recipe.save()

            for form in formset:
                ingredient_name = form.cleaned_data.get('ingredient')
                print(ingredient_name)
                if ingredient_name:
                    ingredient_quantity = form.cleaned_data.get('quantity')
                    ingredient_measurment = form.cleaned_data.get('measurements')
                    print(ingredient_quantity)
                    RecipeIngredient.objects.create(
                        recipe=recipe,
                        ingredient=ingredient_name,
                        quantity=ingredient_quantity,
                        measurements=ingredient_measurment
                    )

            recipe.calculate_macros()

            return redirect('recipes index page')

    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet()

    context = {
        'form': form,
        'formset': formset,
        'ingredients': Ingredient.objects.filter(Q(user=request.user) | Q(user=None)).all()
    }

    return render(request, 'recipes/create_recipe.html', context)


@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    RecipeIngredientFormSet = modelformset_factory(RecipeIngredient, RecipeIngredientForm, extra=3,
                                                   fields=['ingredient', 'quantity', 'measurements'])

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        formset = RecipeIngredientFormSet(request.POST, prefix='ingredient', queryset=recipe.recipeingredient_set.all())

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                recipe = form.save()
                instances = formset.save(commit=False)

                for instance in instances:
                    instance.recipe = recipe
                    instance.save()

        return redirect('show recipes page')


    else:
        form = RecipeForm(instance=recipe)
        formset = RecipeIngredientFormSet(prefix='ingredient', queryset=recipe.recipeingredient_set.all(), )

    context = {
        'form': form,
        'formset': formset,
        'ingredients': Ingredient.objects.filter(Q(user=request.user) | Q(user=None)).all()
    }

    return render(request, 'recipes/edit_recipe.html', context=context)
