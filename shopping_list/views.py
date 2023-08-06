from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import ShoppingList
from .form import ShoppingListForm


class ShowShoppingList(ListView, LoginRequiredMixin):
    model = ShoppingList
    template_name = 'shopping_list/index_shopping_list.html'
    context_object_name = 'shopping_lists'

    def get_queryset(self):
        return ShoppingList.objects.filter(user=self.request.user)


class CreateShoppingList(CreateView, LoginRequiredMixin):
    model = ShoppingList
    form_class = ShoppingListForm
    template_name = 'shopping_list/create_shopping_list.html'
    success_url = reverse_lazy('show shopping lists page')

    def form_valid(self, form):
        shopping_list = form.save(commit=False)
        shopping_list.user = self.request.user
        shopping_list.save()
        form.save_m2m()
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs


class EditShoppingList(UpdateView, LoginRequiredMixin):
    model = ShoppingList
    form_class = ShoppingListForm
    template_name = 'shopping_list/edit_shopping_list.html'
    success_url = reverse_lazy('show shopping list page')

    def get_success_url(self):
        pk = self.kwargs['pk']

        return reverse_lazy('show shopping list page', kwargs={'pk': pk})

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        instance = self.get_object()
        kwargs['user'] = self.request.user
        kwargs['instance'] = instance

        return kwargs

    def get_object(self, queryset=None):
        pk = self.kwargs.get(self.pk_url_kwarg)
        queryset = self.get_queryset().filter(user=self.request.user)
        return get_object_or_404(queryset, pk=pk)


def see_shopping_list(request, pk):
    shopping_list = get_object_or_404(ShoppingList, pk=pk)

    shopping_list_recipes = shopping_list.recipes.all()

    ingredients = {}

    for recipe in shopping_list_recipes:
        print(recipe)

        if recipe not in ingredients:
            ingredients[recipe] = []

        for recipe_ingredient in recipe.recipeingredient_set.all():
            ingredient = recipe_ingredient.ingredient
            quantity = recipe_ingredient.quantity
            measurements = recipe_ingredient.measurements

            ingredient_info = {ingredient: [quantity, measurements]}

            ingredients[recipe].append(ingredient_info)

    print(ingredients)

    context = {
        'recipes': ingredients,
        'shopping_list': shopping_list
    }
    return render(request, 'shopping_list/show_shopping_list.html', context=context)


def delete_shopping_list(request, pk):
    shopping_list = get_object_or_404(ShoppingList, pk=pk)

    if request.method == 'POST':
        shopping_list.delete()
        return redirect('show shopping lists page')

    return render(request, 'shopping_list/delete_shopping_list.html', context={'list': shopping_list})
