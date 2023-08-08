from django.contrib.auth.decorators import login_required, user_passes_test
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


def save_shared_recipe_to_user(user, ingredients, shared_recipe):
    # Checks if the user has all of the ingredients needed for the recipe
    for recipe_ingredient in ingredients:
        ingredient = recipe_ingredient.ingredient

        ingredient_name = ingredient.name
        existing_ingredient = Ingredient.objects.filter(name=ingredient_name, user=user).exists()
        if not existing_ingredient:
            # Gets ingredient data
            calories_per_gram = ingredient.calories_per_gram
            proteins_per_gram = ingredient.proteins_per_gram
            carbs_per_gram = ingredient.carbs_per_gram
            fats_per_gram = ingredient.fats_per_gram
            ingredient_type = ingredient.ingredient_type

            # Creates the ingredient
            new_ingredient = Ingredient(
                name=ingredient_name,
                calories_per_gram=calories_per_gram,
                proteins_per_gram=proteins_per_gram,
                carbs_per_gram=carbs_per_gram,
                fats_per_gram=fats_per_gram,
                ingredient_type=ingredient_type,
                user=user
            )

            new_ingredient.save()

    # Creates the recipe for the user
    saved_recipe = Recipe(
        title=shared_recipe.title,
        instruction=shared_recipe.instruction if shared_recipe.instruction else None,
        user=user
    )
    saved_recipe.save()


    # Transfers the ingredients from the shared recipe to the saved recipe
    for shared_recipe_ingredient in shared_recipe.recipeingredient_set.all():
        ingredient_recipe = RecipeIngredient(
            recipe=saved_recipe,
            ingredient=shared_recipe_ingredient.ingredient,
            quantity=shared_recipe_ingredient.quantity,
            measurements=shared_recipe_ingredient.measurements
        )
        ingredient_recipe.save()

    return saved_recipe

# Gets the shared recipe details and the user can save the recipe
def shared_recipe_details(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    ingredients = recipe.recipeingredient_set.all()

    if request.method == 'POST':
        # Saves the recipe to the user profile
        user_saved_recipe = save_shared_recipe_to_user(request.user, ingredients, recipe)

        return redirect('details recipe page', pk=user_saved_recipe.pk)

    context = {
        'recipe': recipe,
        'ingredients': ingredients
    }

    return render(request, 'recipes/details_shared_recipe.html', context=context)

def user_is_staff(user):
    return user.is_staff and user.has_perm('eat_me_next_tri.can_approve_recipes_for_sharing')


@user_passes_test(user_is_staff)
def approve_recipe(request, pk):
    recipe = get_object_or_404(Recipe, pk=pk)
    ingredients = recipe.recipeingredient_set.all()
    if request.method == 'POST':

        # Lists the recipe for saving
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
        for ingredient in recipe.recipeingredient_set.all():
            ingredient.delete()
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user = self.request.user

        recipes = Recipe.objects.filter(user=user)

        context['recipes'] = recipes

        return context


# Manages data coming from the formset
def manage_formset(formset, recipe):
    for form in formset:

        ingredient_name = form.cleaned_data.get('ingredient')
        ingredient_quantity = form.cleaned_data.get('quantity')
        ingredient_measurment = form.cleaned_data.get('measurements')

        # Creates a new ingredient for the recipe if the form in the formset is valid
        if ingredient_name:
            RecipeIngredient.objects.create(
                recipe=recipe,
                ingredient=ingredient_name,
                quantity=ingredient_quantity,
                measurements=ingredient_measurment
            )

    return True


@login_required
def create_recipe(request):
    RecipeIngredientFormSet = modelformset_factory(form=RecipeIngredientForm, extra=30,
                                                   formset=RecipeIngredientFormUserSetUp,
                                                   model=RecipeIngredient,
                                                   can_delete=True,
                                                   can_delete_extra=True
                                                   )

    if request.method == 'POST':
        form = RecipeForm(request.POST)
        formset = RecipeIngredientFormSet(request.POST, user=request.user, queryset=RecipeIngredient.objects.none())

        if form.is_valid() and formset.is_valid():

            recipe = form.save(commit=False)
            recipe.user = request.user
            recipe.save()
            if manage_formset(formset, recipe):
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
    RecipeIngredientFormSet = modelformset_factory(model=RecipeIngredient, form=RecipeIngredientForm, extra=30,
                                                   formset=RecipeIngredientFormUserSetUp,
                                                   can_delete=True,
                                                   can_delete_extra=True
                                                   )

    if request.method == 'POST':
        form = RecipeForm(request.POST, instance=recipe)
        formset = RecipeIngredientFormSet(request.POST, queryset=recipe.recipeingredient_set.all(),
                                          user=request.user)

        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                recipe = form.save()

                # Deletes all ingredients for the recipe so there won't be any duplicates
                for ingredient in recipe.recipeingredient_set.all():
                    ingredient.delete()

                if manage_formset(formset, recipe):
                    recipe.calculate_macros()
            return redirect('details recipe page', pk=recipe.pk)


    else:
        form = RecipeForm(instance=recipe)
        formset = RecipeIngredientFormSet(queryset=recipe.recipeingredient_set.all(),
                                          user=request.user)

    context = {
        'form': form,
        'formset': formset,
        'ingredients': Ingredient.objects.filter(Q(user=request.user) | Q(user=None)).all()
    }

    return render(request, 'recipes/edit_recipe.html', context=context)
