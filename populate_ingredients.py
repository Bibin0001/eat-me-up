import export as export
import decimal
import requests
import os
import django
from recipes.models import Ingredient

# Set the DJANGO_SETTINGS_MODULE environment variable

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eat_me_next_tri.settings")
# Configure Django settings
django.setup()

API_KEY = '008qP2ON3i25woJDDMrV8wd95EjR1W4qZjILepxd'
INGREDIENT_SEARCH_API = 'https://api.nal.usda.gov/fdc/v1/foods/search'

base_foods = {
    'salt': {
        'calories_per_gram': 0,
        'proteins_per_gram': 0,
        'carbs_per_gram': 0,
        'fats_per_gram': 0
    },
    'pepper': {
        'calories_per_gram': 251,
        'proteins_per_gram': 10.4,
        'carbs_per_gram': 49.9,
        'fats_per_gram': 3.3
    },
    'rice': {
        'calories_per_gram': 130,
        'proteins_per_gram': 2.7,
        'carbs_per_gram': 28.2,
        'fats_per_gram': 0.3
    },
    'pasta': {
        'calories_per_gram': 131,
        'proteins_per_gram': 5.5,
        'carbs_per_gram': 25.1,
        'fats_per_gram': 1.1
    },
    'bread': {
        'calories_per_gram': 266,
        'proteins_per_gram': 8.7,
        'carbs_per_gram': 49.7,
        'fats_per_gram': 4.7
    },
    'chicken breast': {
        'calories_per_gram': 165,
        'proteins_per_gram': 31,
        'carbs_per_gram': 0,
        'fats_per_gram': 3.6
    },
    'beef steak': {
        'calories_per_gram': 250,
        'proteins_per_gram': 26,
        'carbs_per_gram': 0,
        'fats_per_gram': 17
    },
    'salmon': {
        'calories_per_gram': 206,
        'proteins_per_gram': 22,
        'carbs_per_gram': 0,
        'fats_per_gram': 13
    },
    'tofu': {
        'calories_per_gram': 144,
        'proteins_per_gram': 15,
        'carbs_per_gram': 2,
        'fats_per_gram': 9
    },
    'eggs': {
        'calories_per_gram': 143,
        'proteins_per_gram': 12.6,
        'carbs_per_gram': 0.6,
        'fats_per_gram': 9.5
    },
    'milk': {
        'calories_per_gram': 61,
        'proteins_per_gram': 3.3,
        'carbs_per_gram': 4.8,
        'fats_per_gram': 3.3
    },
    'yogurt': {
        'calories_per_gram': 59,
        'proteins_per_gram': 3.5,
        'carbs_per_gram': 4.7,
        'fats_per_gram': 3.3
    },
    'cheese': {
        'calories_per_gram': 402,
        'proteins_per_gram': 25,
        'carbs_per_gram': 1.3,
        'fats_per_gram': 33
    },
    'olive oil': {
        'calories_per_gram': 884,
        'proteins_per_gram': 0,
        'carbs_per_gram': 0,
        'fats_per_gram': 100
    },
    'butter': {
        'calories_per_gram': 717,
        'proteins_per_gram': 0.9,
        'carbs_per_gram': 0.1,
        'fats_per_gram': 81.1
    },
    'sugar': {
        'calories_per_gram': 387,
        'proteins_per_gram': 0,
        'carbs_per_gram': 100,
        'fats_per_gram': 0
    },
    'honey': {
        'calories_per_gram': 304,
        'proteins_per_gram': 0.3,
        'carbs_per_gram': 82,
        'fats_per_gram': 0
    },
    'oats': {
        'calories_per_gram': 389,
        'proteins_per_gram': 16.9,
        'carbs_per_gram': 66.3,
        'fats_per_gram': 6.9
    },
    'potato': {
        'calories_per_gram': 77,
        'proteins_per_gram': 2,
        'carbs_per_gram': 17,
        'fats_per_gram': 0.1
    },
    'sweet potato': {
        'calories_per_gram': 86,
        'proteins_per_gram': 1.6,
        'carbs_per_gram': 20,
        'fats_per_gram': 0.1
    },
    'quinoa': {
        'calories_per_gram': 120,
        'proteins_per_gram': 4.4,
        'carbs_per_gram': 21.3,
        'fats_per_gram': 1.9
    },
    'lentils': {
        'calories_per_gram': 353,
        'proteins_per_gram': 25.8,
        'carbs_per_gram': 63.4,
        'fats_per_gram': 1.1
    },
    'black beans': {
        'calories_per_gram': 339,
        'proteins_per_gram': 21.6,
        'carbs_per_gram': 62.4,
        'fats_per_gram': 0.9
    },
    'chickpeas': {
        'calories_per_gram': 378,
        'proteins_per_gram': 20.5,
        'carbs_per_gram': 60,
        'fats_per_gram': 6
    },
    'almonds': {
        'calories_per_gram': 579,
        'proteins_per_gram': 21.2,
        'carbs_per_gram': 21.7,
        'fats_per_gram': 49.4
    },
    'walnuts': {
        'calories_per_gram': 654,
        'proteins_per_gram': 15.2,
        'carbs_per_gram': 13.7,
        'fats_per_gram': 65.2
    },
    'peanuts': {
        'calories_per_gram': 567,
        'proteins_per_gram': 25.8,
        'carbs_per_gram': 16.1,
        'fats_per_gram': 49.2
    },
    'chocolate': {
        'calories_per_gram': 546,
        'proteins_per_gram': 7.9,
        'carbs_per_gram': 57.5,
        'fats_per_gram': 30.6
    },
    'hummus': {
        'calories_per_gram': 177,
        'proteins_per_gram': 7.9,
        'carbs_per_gram': 17.4,
        'fats_per_gram': 8.7
    },
    'avocado': {
        'calories_per_gram': 160,
        'proteins_per_gram': 2,
        'carbs_per_gram': 9,
        'fats_per_gram': 15
    },
    'spinach': {
        'calories_per_gram': 23,
        'proteins_per_gram': 2.9,
        'carbs_per_gram': 3.6,
        'fats_per_gram': 0.4
    },
    'kale': {
        'calories_per_gram': 49,
        'proteins_per_gram': 4.3,
        'carbs_per_gram': 8.8,
        'fats_per_gram': 0.9
    },
    'tomato': {
        'calories_per_gram': 18,
        'proteins_per_gram': 0.9,
        'carbs_per_gram': 3.9,
        'fats_per_gram': 0.2
    },
    'cucumber': {
        'calories_per_gram': 15,
        'proteins_per_gram': 0.7,
        'carbs_per_gram': 3.6,
        'fats_per_gram': 0.1
    },
    'carrot': {
        'calories_per_gram': 41,
        'proteins_per_gram': 0.9,
        'carbs_per_gram': 10,
        'fats_per_gram': 0.2
    },
    'broccoli': {
        'calories_per_gram': 55,
        'proteins_per_gram': 3.7,
        'carbs_per_gram': 11.2,
        'fats_per_gram': 0.6
    },
    'green beans': {
        'calories_per_gram': 31,
        'proteins_per_gram': 1.8,
        'carbs_per_gram': 7.1,
        'fats_per_gram': 0.2
    },
    'bell pepper': {
        'calories_per_gram': 31,
        'proteins_per_gram': 1.3,
        'carbs_per_gram': 6.3,
        'fats_per_gram': 0.3
    },
    'garlic': {
        'calories_per_gram': 149,
        'proteins_per_gram': 6.4,
        'carbs_per_gram': 33.1,
        'fats_per_gram': 0.5
    },
    'onion': {
        'calories_per_gram': 40,
        'proteins_per_gram': 1.1,
        'carbs_per_gram': 9.3,
        'fats_per_gram': 0.1
    },
    'mushrooms': {
        'calories_per_gram': 22,
        'proteins_per_gram': 3.1,
        'carbs_per_gram': 3.3,
        'fats_per_gram': 0.3
    },
    'bell pepper': {
        'calories_per_gram': 31,
        'proteins_per_gram': 1.3,
        'carbs_per_gram': 6.3,
        'fats_per_gram': 0.3
    },
    'lettuce': {
        'calories_per_gram': 5,
        'proteins_per_gram': 0.5,
        'carbs_per_gram': 1,
        'fats_per_gram': 0.1
    },
    'cabbage': {
        'calories_per_gram': 25,
        'proteins_per_gram': 1.3,
        'carbs_per_gram': 5.8,
        'fats_per_gram': 0.1
    },
    'cauliflower': {
        'calories_per_gram': 25,
        'proteins_per_gram': 1.9,
        'carbs_per_gram': 4.9,
        'fats_per_gram': 0.3
    },
    'asparagus': {
        'calories_per_gram': 20,
        'proteins_per_gram': 2.2,
        'carbs_per_gram': 3.7,
        'fats_per_gram': 0.2
    },
    'green peas': {
        'calories_per_gram': 81,
        'proteins_per_gram': 5,
        'carbs_per_gram': 14,
        'fats_per_gram': 0.4
    },
    'corn': {
        'calories_per_gram': 86,
        'proteins_per_gram': 3.2,
        'carbs_per_gram': 19,
        'fats_per_gram': 1.4
    },
    'black beans': {
        'calories_per_gram': 339,
        'proteins_per_gram': 21.6,
        'carbs_per_gram': 62.4,
        'fats_per_gram': 0.9
    },
    'lentils': {
        'calories_per_gram': 353,
        'proteins_per_gram': 25.8,
        'carbs_per_gram': 63.4,
        'fats_per_gram': 1.1
    },
    'chickpeas': {
        'calories_per_gram': 378,
        'proteins_per_gram': 20.5,
        'carbs_per_gram': 60,
        'fats_per_gram': 6
    },
    'potato': {
        'calories_per_gram': 77,
        'proteins_per_gram': 2,
        'carbs_per_gram': 17,
        'fats_per_gram': 0.1
    },
    'sweet potato': {
        'calories_per_gram': 86,
        'proteins_per_gram': 1.6,
        'carbs_per_gram': 20,
        'fats_per_gram': 0.1
    },
    'quinoa': {
        'calories_per_gram': 120,
        'proteins_per_gram': 4.4,
        'carbs_per_gram': 21.3,
        'fats_per_gram': 1.9
    },
    'brown rice': {
        'calories_per_gram': 111,
        'proteins_per_gram': 2.6,
        'carbs_per_gram': 23.5,
        'fats_per_gram': 0.9
    },
    'whole wheat bread': {
        'calories_per_gram': 250,
        'proteins_per_gram': 10,
        'carbs_per_gram': 47.5,
        'fats_per_gram': 2.5
    },
    'oatmeal': {
        'calories_per_gram': 68,
        'proteins_per_gram': 2.4,
        'carbs_per_gram': 12,
        'fats_per_gram': 1.4
    },
    'whole wheat pasta': {
        'calories_per_gram': 131,
        'proteins_per_gram': 5.5,
        'carbs_per_gram': 25.1,
        'fats_per_gram': 1.1
    },
    'olive oil': {
        'calories_per_gram': 884,
        'proteins_per_gram': 0,
        'carbs_per_gram': 0,
        'fats_per_gram': 100
    },
    'avocado oil': {
        'calories_per_gram': 884,
        'proteins_per_gram': 0,
        'carbs_per_gram': 0,
        'fats_per_gram': 100
    },
    'coconut oil': {
        'calories_per_gram': 862,
        'proteins_per_gram': 0,
        'carbs_per_gram': 0,
        'fats_per_gram': 100
    },
    'canola oil': {
        'calories_per_gram': 884,
        'proteins_per_gram': 0,
        'carbs_per_gram': 0,
        'fats_per_gram': 100
    },
    'soybean oil': {
        'calories_per_gram': 884,
        'proteins_per_gram': 0,
        'carbs_per_gram': 0,
        'fats_per_gram': 100
    },
    'sunflower oil': {
        'calories_per_gram': 884,
        'proteins_per_gram': 0,
        'carbs_per_gram': 0,
        'fats_per_gram': 100
    },
    'corn oil': {
        'calories_per_gram': 884,
        'proteins_per_gram': 0,
        'carbs_per_gram': 0,
        'fats_per_gram': 100
    },
    'butter': {
        'calories_per_gram': 717,
        'proteins_per_gram': 0.9,
        'carbs_per_gram': 0.1,
        'fats_per_gram': 81
    }}
for ingredient, macros in base_foods.items():
    ingredient_name = ingredient
    calories_per_gram = macros['calories_per_gram']
    proteins_per_gram = macros['proteins_per_gram']
    carbs_per_gram = macros['carbs_per_gram']
    fats_per_gram = macros['fats_per_gram']

    ingredient_obj = Ingredient.objects.create(
        name=ingredient_name,
        calories_per_gram=calories_per_gram,
        proteins_per_gram=proteins_per_gram,
        carbs_per_gram=carbs_per_gram,
        fats_per_gram=fats_per_gram
    )

    print(f"Ingredient '{ingredient_obj.name}' added to the database.")

