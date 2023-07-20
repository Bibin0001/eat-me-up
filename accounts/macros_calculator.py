class Macros:
    # TODO: Check if the calories are summed correctly

    def __init__(self, weight, height, age, gender, goal, activity_level):
        self.weight = weight
        self.height = height
        self.age = age
        self.gender = gender
        self.goal = goal
        self.activity_level = activity_level

        self.bmr = self.calculate_bmi()
        self.calories = self.calculate_caloric_intake()
        self.proteins, self.carbs, self.fats = self.calculate_macros()

    def calculate_caloric_intake(self):
        if self.gender == "Male":
            tdee = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) + 5
        else:
            tdee = (10 * self.weight) + (6.25 * self.height) - (5 * self.age) - 161

        # Adjust TDEE based on activity level
        if self.activity_level == "Sedentary":
            tdee *= 1.2
        elif self.activity_level == "Lightly Active":
            tdee *= 1.375
        elif self.activity_level == "Moderately Active":
            tdee *= 1.55
        elif self.activity_level == "Very Active":
            tdee *= 1.725
        elif self.activity_level == "Extra Active":
            tdee *= 1.9

        # Calculate target daily calorie intake for muscle gain
        calories = tdee
        if self.goal == 'Lose Weight':
            calories -= 500
        elif self.goal == 'Gain Weight':
            calories += 500

        return calories

    def calculate_bmi(self):
        if self.gender == 'Male':
            bmr = 88.362 + (13.397 * self.weight) + (4.799 * self.height) - (5.677 * self.age)
        else:
            bmr = 447.593 + (9.247 * self.weight) + (3.098 * self.height) - (4.330 * self.age)

        if self.goal == 'Lose Weight':
            bmr = bmr * 0.8
        elif self.goal == 'Gain Weight':
            bmr = bmr * 1.1
        else:
            bmr = bmr

        return bmr

    def calculate_macros(self):
        protein_calories = self.bmr * 0.3
        carbs_calories = self.bmr * 0.5
        fats_calories = self.bmr * 0.2

        protein_grams = protein_calories / 4
        carbs_grams = carbs_calories / 4
        fats_grams = fats_calories / 9

        return protein_grams, carbs_grams, fats_grams

    def __str__(self):
        return f"Calories : {self.bmr:.2f}\nYou need {self.proteins}protein\n {self.carbs}carbs\n{self.fats}fats. You need calories{self.calories}"


goals = ['weight_loss', 'maintain', 'weight_gain']
#
# rosica = Macros(60, 160, 16, 'Female', goals[0], 'Moderately Active')
# print(rosica)
'''
Needed properties :
    weight in kilograms,
    height in cm,
    age in years 
   
   check this link for instructions:  https://chat.openai.com/
'''
