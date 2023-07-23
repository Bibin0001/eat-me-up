from django.contrib.auth.decorators import login_required
from django.forms import formset_factory
from django.shortcuts import render, redirect
from django.views.generic import CreateView
from django.forms.models import modelformset_factory
from .form import RecipeForm, RecipeIngredientForm
from .models import Recipe, RecipeIngredient
from ingredients.models import Ingredient

# Create your views here.
def index(request):
    return render(request, 'recipes/index.html')


@login_required
def create_recipe(request):
    RecipeIngredientFormSet = formset_factory(RecipeIngredientForm, extra=3)

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
        'ingredients': Ingredient.objects.all()
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
