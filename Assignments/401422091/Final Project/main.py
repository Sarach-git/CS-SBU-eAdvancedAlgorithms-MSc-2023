import pandas as pd
from pulp import *
import random


def calculate_tte():
    # Take age, gender, height and weight from the user
    age = int(input('What is your age? '))
    gender = input('What is your gender? (M/F): ')
    height = float(input('What is your height? (in CM): '))
    weight = float(input('What is your weight? (in KG): '))

    # Calculate BMR
    if gender.lower() == 'm':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

    # Calculate TTE (because they want to be active, I chose 1.7)
    # TTE is stands on Total Energy Expenditure
    calculated_tte = bmr * 1.7

    return calculated_tte


tte = calculate_tte()

# Read the USDA dataset
df = pd.read_csv('USDA.csv')
df = df.dropna(axis=0, how='any')
df.drop_duplicates(subset=None, inplace=True)

# List of ingredients
ingredients = list(df['Description'])

# List of ingredients followed by their calorie amount
ingredient_calorie_map = dict(zip(ingredients, df['Calories']))

# List of ingredients followed by their protein amount
ingredient_protein_map = dict(zip(ingredients, df['Protein']))

# List of ingredients followed by their total fat amount
ingredient_total_fat_map = dict(zip(ingredients, df['TotalFat']))

# List of ingredients followed by their carbohydrate amount
ingredient_carbohydrate_map = dict(zip(ingredients, df['Carbohydrate']))

# List of ingredients followed by their iron amount
ingredient_iron_map = dict(zip(ingredients, df['Iron']))

# DRI stands on Dietary Reference Intake which is the amount of nutritious  every individual can intake in a day
# Our constraints consist of minimum and maximum of DRI for a day

# Define minimum constraints for Fat, Carbohydrate, Protein, and Iron for athletes and someone who wants to lose weight
min_calories = tte - 200
min_fat = 0.25 * tte / 9
min_carbohydrate = 0.50 * tte / 4
min_protein = 0.15 * tte / 4
min_iron = 0.0043 * tte

# Define maximum constraints
max_calories = tte + 200
max_fat = 0.4 * tte / 9
max_carbohydrate = 0.7 * tte / 4
max_protein = 0.4 * tte / 4
max_iron = 0.009 * tte

# Define linear programming problem
problem = LpProblem('Diet_plan', LpMinimize)
food_vars = LpVariable.dicts('Food', ingredients, 0, cat='Integer')

# Calories
problem += lpSum([ingredient_calorie_map[f] * food_vars[f] for f in ingredients]) >= min_calories, 'CaloriesMinimum'
problem += lpSum([ingredient_calorie_map[f] * food_vars[f] for f in ingredients]) <= max_calories, 'CaloriesMaximum'

# Fat
problem += lpSum([ingredient_total_fat_map[f] * food_vars[f] for f in ingredients]) >= min_fat, 'FatMinimum'
problem += lpSum([ingredient_total_fat_map[f] * food_vars[f] for f in ingredients]) <= max_fat, 'FatMaximum'

# Carbohydrate
problem += lpSum(
    [ingredient_carbohydrate_map[f] * food_vars[f] for f in ingredients]) >= min_carbohydrate, 'CarbsMinimum'
problem += lpSum(
    [ingredient_carbohydrate_map[f] * food_vars[f] for f in ingredients]) <= max_carbohydrate, 'CarbsMaximum'

# Protein
problem += lpSum([ingredient_protein_map[f] * food_vars[f] for f in ingredients]) >= min_protein, 'ProteinMinimum'
problem += lpSum([ingredient_protein_map[f] * food_vars[f] for f in ingredients]) <= max_protein, 'ProteinMaximum'

# Iron
problem += lpSum([ingredient_iron_map[f] * food_vars[f] for f in ingredients]) >= min_iron, 'IronMinimum'
problem += lpSum([ingredient_iron_map[f] * food_vars[f] for f in ingredients]) <= max_iron, 'IronMaximum'

problem.solve(PULP_CBC_CMD(msg=False))

# List of meals
meals = ['Breakfast', 'Morning snack', 'Lunch', 'Afternoon snack', 'Dinner']

# List of meals followed by their list of ingredients
meals_dict = {
    'Breakfast': [],
    'Morning snack': [],
    'Lunch': [],
    'Afternoon snack': [],
    'Dinner': []
}

if LpStatus[problem.status] == 'Optimal':
    total_calories = 0
    total_fat = 0
    total_carbohydrate = 0
    total_protein = 0
    total_iron = 0

    # Obtain ingredients with varValue more than zero
    suitable_ingredients_list = []
    for ingredient in ingredients:
        food_var = food_vars[ingredient]
        if food_var.varValue is not None and food_var.varValue > 0:
            suitable_ingredients_list.append(ingredient)

    random.shuffle(suitable_ingredients_list)

    # Put the ingredients in meals dict almost evenly
    for index, ingredient in enumerate(suitable_ingredients_list):
        food_var = food_vars[ingredient]
        ingredient_amount = food_var.varValue
        ing_fat = ingredient_total_fat_map.get(ingredient, 0) * ingredient_amount
        ing_calories = ingredient_calorie_map.get(ingredient, 0) * ingredient_amount
        ing_carbohydrate = ingredient_carbohydrate_map.get(ingredient, 0) * ingredient_amount
        ing_protein = ingredient_protein_map.get(ingredient, 0) * ingredient_amount
        ing_iron = ingredient_iron_map.get(ingredient, 0) * ingredient_amount

        total_fat += ing_fat
        total_calories += ing_calories
        total_carbohydrate += ing_carbohydrate
        total_protein += ing_protein
        total_iron += ing_iron
        meals_dict[meals[index % len(meals)]].append(
            [ingredient, ingredient_amount, ing_fat, ing_calories, ing_carbohydrate, ing_protein, ing_iron])

    # Find ingredient which doesn't break the constraints
    additional_items = []
    for ingredient in ingredients:
        food_var = food_vars[ingredient]
        ingredient_amount = 1.0
        ing_fat = ingredient_total_fat_map.get(ingredient, 0) * ingredient_amount
        ing_calorie = ingredient_calorie_map.get(ingredient, 0) * ingredient_amount
        ing_carbohydrate = ingredient_carbohydrate_map.get(ingredient, 0) * ingredient_amount
        ing_protein = ingredient_protein_map.get(ingredient, 0) * ingredient_amount
        ing_iron = ingredient_iron_map.get(ingredient, 0) * ingredient_amount
        if ing_fat + total_fat < max_fat and ing_carbohydrate + total_carbohydrate < max_carbohydrate \
                and ing_protein + total_protein < max_protein and ing_iron + total_iron < max_iron \
                and ing_calorie + total_calories < max_calories:
            total_fat += ing_fat
            total_calories += ing_calorie
            total_carbohydrate += ing_carbohydrate
            total_protein += ing_protein
            total_iron += ing_iron
            additional_items.append(
                [ingredient, ingredient_amount, ing_fat, ing_calorie, ing_carbohydrate, ing_protein, ing_iron])
    # Add additional items to the meals almost evenly
    for index, item in enumerate(additional_items):
        meals_dict[meals[index % len(meals)]].append(item)

    # Print the output and calculate every meal nutritional content
    for meal, data in meals_dict.items():
        meal_fat = 0
        meal_calories = 0
        meal_carbohydrate = 0
        meal_protein = 0
        meal_iron = 0
        print(f'- {meal}')
        for item in data:
            print(f'    - {item[1]} {item[0]}')
            meal_fat += item[2]
            meal_calories += item[3]
            meal_carbohydrate += item[4]
            meal_protein += item[5]
            meal_iron += item[6]
        print(
            f'(Nutritional Content: Calories: {meal_calories}, Fat: {meal_fat}, Carbohydrate: {meal_carbohydrate}, Protein: {meal_protein}, Iron: {meal_iron})')
        print()

    print(
        f'Total Nutritional Content (for all of meals together): Calories: {total_calories}, Fat: {total_fat}, Carbohydrate: {total_carbohydrate}, Protein: {total_protein}, Iron: {total_iron}')
else:
    print('There is no solution with your input')
