import pandas as pd
from pulp import *
import random

# Read the USDA dataset
df = pd.read_csv("C:/Users/Poosmal/Downloads/USDA.csv")
df = df.dropna(axis=0, how='any')
df.drop_duplicates(subset=None, inplace=True)

# Create a dictionary to store activity multipliers based on activity level
activity_multipliers = {
    'sedentary': 1.2,
    'lightly_active': 1.375,
    'moderately_active': 1.55,
    'very_active': 1.725,
    'extra_active': 1.9
}

# Take input from the user
age = int(input("Enter your age: "))
gender = input("Enter your gender (M/F): ")
height = float(input("Enter your height (in cm): "))
weight = float(input("Enter your weight (in kg): "))
activity_level = input("Enter your activity level (sedentary, lightly_active, moderately_active, very_active, extra_active): ")

# Calculate BMR based on age, gender, height, and weight
if gender.lower() == 'm':
    bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
else:
    bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)

# Calculate TTE by multiplying BMR with activity level multiplier
activity_multiplier = activity_multipliers.get(activity_level.lower(), 1.2)
tte = bmr * activity_multiplier

print("Basal Metabolic Rate (BMR):", bmr)
print("Total Energy Expenditure (TTE):", tte)

prob = LpProblem("Meal_Diet_Problem", LpMinimize)

# Creates a list of the Ingredients
food_items = list(df['Description'])
calories = dict(zip(food_items, df['Calories']))
protein = dict(zip(food_items, df['Protein']))
totalFat = dict(zip(food_items, df['TotalFat']))
carbohydrate = dict(zip(food_items, df['Carbohydrate']))
iron = dict(zip(food_items, df['Iron']))

food_vars = LpVariable.dicts("Food", food_items, 0, cat='Integer')

# Set constraints for Fat, Carbohydrate, Protein, and Iron
fat_dri = 0.25 * tte / 9  # DRI for Fat (25% of TTE)
carb_dri = 0.5 * tte / 4  # DRI for Carbohydrate (50% of TTE)
protein_dri = 0.15 * tte / 4  # DRI for Protein (15% of TTE)
iron_dri = 0.0043 * tte  # DRI for Iron (0.43% of TTE)

# Define maximum constraint values
max_fat = 0.35 * tte / 9
max_carb = 0.65 * tte / 4
max_protein = 0.35 * tte / 4
max_iron = 2 * (0.0043 * tte)

# Set the objective function to minimize total calories
prob += lpSum([calories[f] * food_vars[f] for f in food_items]), "TotalCalories"

# Calories
prob += lpSum([calories[f] * food_vars[f] for f in food_items]) >= tte-200, "CaloriesMinimum"
prob += lpSum([calories[f] * food_vars[f] for f in food_items]) <= tte + 200, "CaloriesMaximum"

# Fat
prob += lpSum([totalFat[f] * food_vars[f] for f in food_items]) >= fat_dri, "FatMinimum"
prob += lpSum([totalFat[f] * food_vars[f] for f in food_items]) <= max_fat, "FatMaximum"

# Carbohydrate
prob += lpSum([carbohydrate[f] * food_vars[f] for f in food_items]) >= carb_dri, "CarbsMinimum"
prob += lpSum([carbohydrate[f] * food_vars[f] for f in food_items]) <= max_carb, "CarbsMaximum"

# Protein
prob += lpSum([protein[f] * food_vars[f] for f in food_items]) >= protein_dri, "ProteinMinimum"
prob += lpSum([protein[f] * food_vars[f] for f in food_items]) <= max_protein, "ProteinMaximum"

# Iron
prob += lpSum([iron[f] * food_vars[f] for f in food_items]) >= iron_dri, "IronMinimum"
prob += lpSum([iron[f] * food_vars[f] for f in food_items]) <= max_iron, "IronMaximum"

prob.solve()

print("Status:", LpStatus[prob.status])

meal_percentages = {
    'breakfast': 0.25,
    'morning_snack': 0.1,
    'lunch': 0.3,
    'afternoon_snack': 0.1,
    'dinner': 0.25
}

if LpStatus[prob.status] == 'Optimal':
    total_calories = value(prob.objective)
    total_fat = 0
    total_carbohydrate = 0
    total_iron = 0

    # Create empty meal lists
    meals = {meal: [] for meal in meal_percentages.keys()}

    # Distribute food items into meals
    for food_item in food_items:
        food_var = food_vars[food_item]
        if food_var.varValue is not None and food_var.varValue > 0:
            food_amount = food_var.varValue

            # Select a random meal based on the percentages
            meal = random.choices(list(meal_percentages.keys()), list(meal_percentages.values()))[0]

            # Append the food item to the selected meal
            meals[meal].append((food_item, food_amount))

            # Calculate total nutritional values
            food_fat = totalFat.get(food_item, 0)
            food_carbohydrate = carbohydrate.get(food_item, 0)
            food_iron = iron.get(food_item, 0)

            total_fat += food_amount * food_fat
            total_carbohydrate += food_amount * food_carbohydrate
            total_iron += food_amount * food_iron

    # Check if any meals are empty and assign one food item randomly to each empty meal
    empty_meals = [meal for meal, items in meals.items() if not items]
    for meal in empty_meals:
        food_item = random.choice(food_items)
        food_amount = 1  # Assign a fixed amount of 1 for simplicity

        meals[meal].append((food_item, food_amount))

        # Update the total nutritional values
        food_fat = totalFat.get(food_item, 0)
        food_carbohydrate = carbohydrate.get(food_item, 0)
        food_iron = iron.get(food_item, 0)

        total_fat += food_amount * food_fat
        total_carbohydrate += food_amount * food_carbohydrate
        total_iron += food_amount * food_iron

    print("-" * 110)
    print("Total Calories:", total_calories)
    print("Total Fat:", total_fat)
    print("Total Carbohydrate:", total_carbohydrate)
    print("Total Iron:", total_iron)

    # Print the final meal plan
    print("\nMeal Plan:")
    print("-" * 110)
    for meal, items in meals.items():
        meal_calories = sum(calories[food_item] * food_amount for food_item, food_amount in items)
        meal_fat = sum(totalFat[food_item] * food_amount for food_item, food_amount in items)
        meal_carbohydrate = sum(carbohydrate[food_item] * food_amount for food_item, food_amount in items)
        meal_iron = sum(iron[food_item] * food_amount for food_item, food_amount in items)

        print(f"{meal.capitalize()}:")
        for food_item, food_amount in items:
            print(f"- {food_item}: {food_amount} g")

        print(f"Total Calories: {meal_calories}")
        print(f"Total Fat: {meal_fat} g")
        print(f"Total Carbohydrate: {meal_carbohydrate} g")
        print(f"Total Iron: {meal_iron} mg")
        print("-" * 110)
else:
    print("No solution found.")
