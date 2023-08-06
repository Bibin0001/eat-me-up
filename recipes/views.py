from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Q
from django.forms import formset_factory, BaseFormSet
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.forms.models import modelformset_factory
from .form import RecipeForm, RecipeIngredientForm, RecipeIngredientFormUserSetUp
from .models import Recipe, RecipeIngredient, SavedRecipes
from ingredients.models import Ingredient
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.forms import formset_factory


def shared_recipe_details(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    ingredients = recipe.recipeingredient_set.all()

    if request.method == 'POST':
        if not SavedRecipes.objects.filter(user=request.user, recipe=recipe).exists():
            saved_recipe = SavedRecipes(user=request.user, recipe=recipe)
            saved_recipe.save()

        for recipe_ingredient in ingredients:
            ingredient = recipe_ingredient.ingredient

            ingredient_name = ingredient.name
            calories_per_gram = ingredient.calories_per_gram
            proteins_per_gram = ingredient.proteins_per_gram
            carbs_per_gram = ingredient.carbs_per_gram
            fats_per_gram = ingredient.fats_per_gram
            ingredient_type = ingredient.ingredient_type

            existing_ingredient = Ingredient.objects.filter(name=ingredient_name, user=request.user).exists()

            if not existing_ingredient:
                new_ingredient = not Ingredient(
                    name=ingredient_name,
                    calories_per_gram=calories_per_gram,
                    proteins_per_gram=proteins_per_gram,
                    carbs_per_gram=carbs_per_gram,
                    fats_per_gram=fats_per_gram,
                    ingredient_type=ingredient_type,
                    user=request.user
                )

                new_ingredient.save()

        return redirect('show shared recipes page')

    context = {
        'recipe': recipe,
        'ingredients': ingredients
    }

    return render(request, 'recipes/details_shared_recipe.html', context=context)


def approve_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    ingredients = recipe.recipeingredient_set.all()
    if request.method == 'POST':

        if 'approve' in request.POST:
            recipe.approved_for_sharing = True
            recipe.share = False

        else:
            recipe.share = False

        recipe.save()

        return redirect('show pending recipes page')

    context = {
        'recipe': recipe,
        'ingredients': ingredients
    }

    return render(request, 'recipes/approve_recipe.html', context=context)


class ShowPendingRecipes(ListView, UserPassesTestMixin):
    template_name = 'recipes/show_pending_recipes.html'
    model = Recipe
    context_object_name = 'recipes'

    def test_func(self):
        return self.request.user.is_staff

    def get_queryset(self):
        query_set = Recipe.objects.filter(share=True)
        return query_set


def delete_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)

    if request.method == 'POST':
        recipe.delete()

        return redirect('show recipes page')

    context = {
        'recipe': recipe
    }

    return render(request, 'recipes/delete_recipe.html', context=context)


def recipe_details(request, pk):
    recipe = Recipe.objects.get(pk=pk)
    ingredients = recipe.recipeingredient_set.all()
    context = {
        'recipe': recipe,
        'ingredients': ingredients
    }

    return render(request, 'recipes/details_recipe.html', context=context)




class ShowSharedRecipes(ListView, LoginRequiredMixin):
    model = Recipe
    template_name = 'recipes/show_shared_recipes.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        return Recipe.objects.filter(approved_for_sharing=True)


class ShowUserRecipes(ListView, LoginRequiredMixin):
    model = Recipe
    template_name = 'recipes/show_recipes.html'
    context_object_name = 'recipes'

    def get_queryset(self):
        user = self.request.user

        user_recipes = Recipe.objects.filter(user=user)
        saved_recipes = Recipe.objects.filter(user=user)

        queryset = user_recipes | saved_recipes

        return queryset


@login_required
def create_recipe(request):
    RecipeIngredientFormSet = modelformset_factory(form=RecipeIngredientForm, extra=30,
                                                   formset=RecipeIngredientFormUserSetUp,
                                                   model=RecipeIngredient)

    if request.method == 'POST':
        form = RecipeForm(request.POST)
        formset = RecipeIngredientFormSet(request.POST, user=request.user, queryset=RecipeIngredient.objects.none())

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
            return redirect('details recipe page', pk=recipe.pk)

    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet(user=request.user, queryset=RecipeIngredient.objects.none())

    context = {
        'form': form,
        'formset': formset,
        'ingredients': Ingredient.objects.filter(Q(user=request.user) | Q(user=None)).all()
    }

    return render(request, 'recipes/create_recipe.html', context)


@login_required
def edit_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    RecipeIngredientFormSet = modelformset_factory(RecipeIngredient, RecipeIngredientForm, extra=30,
                                                   fields=['ingredient', 'quantity', 'measurements'],
                                                   formset=RecipeIngredientFormUserSetUp)

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        formset = RecipeIngredientFormSet(request.POST, prefix='ingredient', queryset=recipe.recipeingredient_set.all(),
                                          user=request.user)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                recipe = form.save()
                instances = formset.save(commit=False)

                for instance in instances:
                    instance.recipe = recipe
                    instance.save()

        return redirect('details recipe page', pk=recipe.pk)


    else:
        form = RecipeForm(instance=recipe)
        formset = RecipeIngredientFormSet(prefix='ingredient', queryset=recipe.recipeingredient_set.all(),
                                          user=request.user)

    context = {
        'form': form,
        'formset': formset,
        'ingredients': Ingredient.objects.filter(Q(user=request.user) | Q(user=None)).all()
    }

    return render(request, 'recipes/edit_recipe.html', context=context)
