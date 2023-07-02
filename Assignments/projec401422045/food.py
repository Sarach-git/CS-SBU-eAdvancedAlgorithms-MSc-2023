import random
import csv
from pulp import *
import warnings

# Ignore all warnings
warnings.filterwarnings("ignore")


# Function to load the USDA dataset from CSV
def load_usda_dataset(file_path):
    dataset = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        next(reader)  # Skip the header row
        for row in reader:
            item = {
                'ID': row[0] if row[0] != '' else None,
                'Description': row[1] if row[1] != '' else None,
                'Calories': float(row[2]) if row[2] != '' else None,
                'Protein': float(row[3]) if row[3] != '' else None,
                'TotalFat': float(row[4]) if row[4] != '' else None,
                'Carbohydrate': float(row[5]) if row[5] != '' else None,
                'Sodium': float(row[6]) if row[6] != '' else None,
                'SaturatedFat': float(row[7]) if row[7] != '' else None,
                'Cholesterol': float(row[8]) if row[8] != '' else None,
                'Sugar': float(row[9]) if row[9] != '' else None,
                'Calcium': float(row[10]) if row[10] != '' else None,
                'Iron': float(row[11]) if row[11] != '' else None,
                'Potassium': float(row[12]) if row[12] != '' else None,
                'VitaminC': float(row[13]) if row[13] != '' else None,
                'VitaminE': float(row[14]) if row[14] != '' else None,
                'VitaminD': float(row[15]) if row[15] != '' else None
            }
            dataset.append(item)
    return dataset

# Load the USDA dataset
usda_file_path = 'USDA.csv'
usda_dataset_main = load_usda_dataset(usda_file_path)

# Define the user's weight, height, sex, and dietary preferences

weight = int(input("Enter your weight in kilograms: "))


def return_mill(s_dataset_1 , mill_factor , key_words, mill):
    if(key_words):
        s_dataset = [item for item in s_dataset_1 if any(word in item['Description'].lower() for word in key_words)]
    else :
        s_dataset = s_dataset_1
    # Define the health.gov guidelines (simplified version)
    guidelines = {
        'calories_min': mill_factor['calories_min']*weight * 25,     # Minimum calories based on weight (kcal)
        'calories_max': mill_factor['calories_max']*weight * 30,     # Maximum calories based on weight (kcal)
        'protein_min': mill_factor['protein_min']*weight * 0.8,     # Minimum protein based on weight (g)
        'fat_max': mill_factor['fat_max']*weight * 0.4,         # Maximum fat based on weight (g)
        'carbs_min': mill_factor['carbs_min']*weight * 2,         # Minimum carbohydrates based on weight (g)
        'sodium_max': mill_factor['sodium_max']*2300,              # Maximum sodium intake (mg)
        'saturated_fat_max': mill_factor['saturated_fat_max']*20,         # Maximum saturated fat intake (in grams)
        'cholesterol_max': mill_factor['cholesterol_max']*300,          # Maximum cholesterol intake (in milligrams)
        'sugar_max': mill_factor['sugar_max']*50,                 # Maximum sugar intake (in grams)
        'calcium_min': mill_factor['calcium_min']*1000,             # Minimum calcium intake (in milligrams)
        'iron_min': mill_factor['iron_min']*8,                   # Minimum iron intake (in milligrams)
        'potassium_min': mill_factor['potassium_min']*3500,           # Minimum potassium intake (in milligrams)
        'vitamin_c_min': mill_factor['vitamin_c_min']*90,             # Minimum vitamin C intake (in milligrams)
        'vitamin_e_min': mill_factor['vitamin_e_min']*15,             # Minimum vitamin E intake (in milligrams)
        'vitamin_d_min': mill_factor['vitamin_d_min']*15              # Minimum vitamin D intake (in micrograms)
    }

    # Create the LP problem
    problem = LpProblem("Diet Problem", LpMaximize)

    # Create decision variables for each item in the dataset
    items = LpVariable.dicts("Item", [item['ID'] for item in s_dataset], 0, 1, LpInteger)


    # Define the objective function: maximize ingredient variety
    problem += lpSum(items[item['ID']] if item['ID'] in items else 0 for item in s_dataset)
    problem += lpSum(items[item['ID']] for item in s_dataset) == 2


    # Guideline constraints
    problem += lpSum(items[item['ID']] * item['Calories'] if item['Calories'] is not None else 0 for item in s_dataset) >= guidelines['calories_min']
    problem += lpSum(items[item['ID']] * item['Calories'] if item['Calories'] is not None else 0 for item in s_dataset) <= guidelines['calories_max']
    problem += lpSum(items[item['ID']] * item['Protein'] if item['Protein'] is not None else 0 for item in s_dataset) >= guidelines['protein_min']
    problem += lpSum(items[item['ID']] * item['TotalFat'] if item['TotalFat'] is not None else 0 for item in s_dataset) <= guidelines['fat_max']
    problem += lpSum(items[item['ID']] * item['Carbohydrate'] if item['Carbohydrate'] is not None else 0 for item in s_dataset) >= guidelines['carbs_min']
    problem += lpSum(items[item['ID']] * item['Sodium'] if item['Sodium'] is not None else 0 for item in s_dataset) <= guidelines['sodium_max']
    problem += lpSum(items[item['ID']] * item['SaturatedFat'] if item['SaturatedFat'] is not None else 0 for item in s_dataset) <= guidelines['saturated_fat_max']
    problem += lpSum(items[item['ID']] * item['Cholesterol'] if item['Cholesterol'] is not None else 0 for item in s_dataset) <= guidelines['cholesterol_max']
    problem += lpSum(items[item['ID']] * item['Sugar'] if item['Sugar'] is not None else 0 for item in s_dataset) <= guidelines['sugar_max']
    problem += lpSum(items[item['ID']] * item['Calcium'] if item['Calcium'] is not None else 0 for item in s_dataset) >= guidelines['calcium_min']
    problem += lpSum(items[item['ID']] * item['Iron'] if item['Iron'] is not None else 0 for item in s_dataset) >= guidelines['iron_min']
    problem += lpSum(items[item['ID']] * item['Potassium'] if item['Potassium'] is not None else 0 for item in s_dataset) >= guidelines['potassium_min']
    problem += lpSum(items[item['ID']] * item['VitaminC'] if item['VitaminC'] is not None else 0 for item in s_dataset) >= guidelines['vitamin_c_min']
    problem += lpSum(items[item['ID']] * item['VitaminE'] if item['VitaminE'] is not None else 0 for item in s_dataset) >= guidelines['vitamin_e_min']



    # Add dietary preferences constraint (e.g., vegan)
    # for item in s_dataset:
    #     if 'vegan' in dietary_preferences and 'Vegan' not in item['Description']:
    #         problem += items[item['ID']] == 0

    # Solve the LP problem
    problem.solve()

    # Get the selected items (meals)
    selected_items = [item for item in s_dataset if items[item['ID']].varValue == 1]

    # Print the selected items (meals) with food compositions
    print("meals:" + mill)
    for i, item in enumerate(selected_items, start=1):
        print(f"   - {item['Description']}")



#breakfast
breakfast = {
'calories_min' : 0.25 ,
'calories_max' : 0.25 ,
'protein_min' : 0.25 ,
'fat_max' : 0.25 ,
'carbs_min' : 0.25 ,
'sodium_max' : 0.25 ,
'saturated_fat_max' : 0.25 ,
'cholesterol_max' : 0.25 ,
'sugar_max' : 0.25 ,
'calcium_min' : 0.25 ,
'iron_min' : 0.25 ,
'potassium_min' : 0.25 ,
'vitamin_c_min' : 0.25 ,
'vitamin_e_min' : 0 ,
'vitamin_d_min' : 0 ,
}
#breakfast
lunch = {
'calories_min' : 0.35 ,
'calories_max' : 0.35 ,
'protein_min' : 0.35 ,
'fat_max' : 0.35 ,
'carbs_min' : 0.35 ,
'sodium_max' : 0.35 ,
'saturated_fat_max' : 0.35 ,
'cholesterol_max' : 0.35 ,
'sugar_max' : 0.35 ,
'calcium_min' : 0.35 ,
'iron_min' : 0.35 ,
'potassium_min' : 0.35 ,
'vitamin_c_min' : 0.35 ,
'vitamin_e_min' : 0 ,
'vitamin_d_min' : 0 ,
}
#breakfast
diner = {
'calories_min' : 0.30 ,
'calories_max' : 0.30 ,
'protein_min' : 0.30 ,
'fat_max' : 0.30 ,
'carbs_min' : 0.30 ,
'sodium_max' : 0.30 ,
'saturated_fat_max' : 0.30 ,
'cholesterol_max' : 0.30 ,
'sugar_max' : 0.30 ,
'calcium_min' : 0.30 ,
'iron_min' : 0.30 ,
'potassium_min' : 0.30 ,
'vitamin_c_min' : 0.30 ,
'vitamin_e_min' : 0.5 ,
'vitamin_d_min' : 1 ,
}
#breakfast
evening = {
'calories_min' : 0.10 ,
'calories_max' : 0.10 ,
'protein_min' : 0.10 ,
'fat_max' : 0.10 ,
'carbs_min' : 0.10 ,
'sodium_max' : 0.10 ,
'saturated_fat_max' : 0.10 ,
'cholesterol_max' : 0.10 ,
'sugar_max' : 0.10 ,
'calcium_min' : 0.10 ,
'iron_min' : 0.10 ,
'potassium_min' : 0.10 ,
'vitamin_c_min' : 0.10 ,
'vitamin_e_min' : 0.5 ,
'vitamin_d_min' : 1 ,
}

key_words = ['milk', 'egg', 'meat', 'Orange']  # List of key words
return_mill(usda_dataset_main , breakfast , key_words , 'breakfast')

return_mill(usda_dataset_main , lunch , False , 'lunch')

return_mill(usda_dataset_main , diner , False , 'diner')

return_mill(usda_dataset_main , evening , False , 'evening snak')


