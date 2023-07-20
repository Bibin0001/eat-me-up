from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.forms.models import modelformset_factory
from .form import RecipeForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient, Ingredient


# Create your views here.
def index(request):
    return render(request, 'recipes/index.html')


def create_recipe(request):
    RecipeIngredientFormSet = formset_factory(RecipeIngredientForm, extra=30)

    if request.method == 'POST':
        form = RecipeForm(request.POST)
        formset = RecipeIngredientFormSet(request.POST)

        if form.is_valid() and formset.is_valid():
            print(form.cleaned_data)
            print(formset.cleaned_data)
            ingredients = []

            total_calories = 0
            total_proteins = 0
            total_carbs = 0
            total_fats = 0
            for form in formset:
                ingredient_data = form.cleaned_data.get('ingredient')

                if ingredient_data:

                # ingredients.append(form.cleaned_data['ingredient'])

            print(f"Ingredients: {ingredients}")
            return redirect('home page')

    else:
        form = RecipeForm()
        formset = RecipeIngredientFormSet()

    context = {
        'form': form,
        'formset': formset
    }

    return render(request, 'recipes/create_recipe.html', context)


class RecipeCreateView(CreateView):
    model = Recipe
    form_class = RecipeForm
    template_name = 'recipes/create_recipe.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        RecipeIngredientFormset = modelformset_factory(
            RecipeIngredient,
            form=RecipeIngredientForm,
            extra=1,
            can_delete=True
        )

        if self.request.POST:
            context['formset'] = RecipeIngredientFormset(self.request.POST, prefix='ingredient')
        else:
            context['formset'] = RecipeIngredientFormset(prefix='ingredient')

        return context

    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']

        if formset.is_valid():
            self.object = form.save()

            instances = formset.save(commit=False)
            for instance in instances:
                instance.recipe = self.object
                instance.save()

            return redirect('home page')

        return self.render_to_response(self.get_context_data(form=form))
