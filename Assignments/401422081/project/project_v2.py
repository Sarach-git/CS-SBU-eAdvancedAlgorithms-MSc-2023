# Import all classes of PuLP module
from pulp import *
import pulp as pl
import pandas


problem = LpProblem('Diet Problem', LpMaximize)

x = [] #Initialize objective variables
xCoefficients = []

pandas.set_option('display.max_rows', None)
foods = pandas.read_csv('/home/mahsaa/Desktop/CS-SBU-eAdvancedAlgorithms-MSc-2023/Assignments/401422081/project/food.csv') #fdc_id, description, food_category_id 
category = pandas.read_csv('/home/mahsaa/Desktop/CS-SBU-eAdvancedAlgorithms-MSc-2023/Assignments/401422081/project/food_category.csv') #id, description
nutrient = pandas.read_csv('/home/mahsaa/Desktop/CS-SBU-eAdvancedAlgorithms-MSc-2023/Assignments/401422081/project/food_nutrient.csv') #fdc_id, nutrient_id
ingredients = pandas.read_csv('/home/mahsaa/Desktop/CS-SBU-eAdvancedAlgorithms-MSc-2023/Assignments/401422081/project/input_food.csv') #fdc_id, fdc_of_input_food
#nutrient ids -> 1003 protein, 1004 fat, 1005 carbo
totalCalories = 0
for i in range(0,100):
    foodId = foods.iloc[i]['fdc_id']
    foodDescription = foods.iloc[i]['description']
    nutrientRows = nutrient.query(f'fdc_id == {foodId}')
    calories = 0
    calories += nutrientRows.query(f'nutrient_id == 1003') * 4
    calories += nutrientRows.query(f'nutrient_id == 1004') * 9
    calories += nutrientRows.query(f'nutrient_id == 1005') * 4
    print(f'foodId: {foodId} - desc: {foodDescription} - calory: {nutrientRows}')
    

# for i in range(0,100):
    # print(df.iloc[i]['Calories'])
    # totalCalories += foods.iloc[i]['Calories']
    # x.append(LpVariable(str( foods.iloc[i]['ID']), range(1), cat=LpBinary))
    # xCoefficients.append(foods.iloc[i]['Calories'])
# problem += lpSum(x[i] * xCoefficients[i] for i in range(0, len(x)))
# print("Total calories: ", totalCalories) 
# print("Current Status: ", LpStatus[problem.status]) 
# problem.solve()
# print("Objective: ", value(problem.objective))