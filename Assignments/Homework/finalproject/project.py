# -*- coding: utf-8 -*-
"""
@author: persian
"""

#pip install -U git+https://github.com/coin-or/pulp

import pandas as pd
import numpy as np
from pulp import *

df = pd.read_csv('USDA.csv')
df = df.fillna(0)



data = np.array(df)
data[data == None] = 0

Calories_ = data[:,2].astype(np.float64)
Protein_ = data[:,3].astype(np.float64)
TotalFat_ = data[:,4].astype(np.float64)
Carbohydrate_ = data[:,5].astype(np.float64)
Sodium_  = data[:,6].astype(np.float64)
SaturatedFat_ = data[:,7].astype(np.float64)
Cholesterol_ =  data[:,8].astype(np.float64)
Sugar_ = data[:,9].astype(np.float64)
Calcium_ = data[:,10].astype(np.float64)
Iron_ = data[:,11].astype(np.float64)
Potassium_ = data[:,12].astype(np.float64)
VitaminC_ = data[:,13].astype(np.float64) 
VitaminE_ =  data[:,14].astype(np.float64)
VitaminD_  = data[:,15].astype(np.float64)


cost = np.random.uniform(100, size=(data.shape[0],1))


food_items = list(df['Description'])

calories = dict(zip(food_items,Calories_))

cholesterol = dict(zip(food_items,Cholesterol_))

fat = dict(zip(food_items,TotalFat_))

sodium = dict(zip(food_items,Sodium_))

carbs = dict(zip(food_items,Carbohydrate_))

protein = dict(zip(food_items,Protein_))

vit_C = dict(zip(food_items,VitaminC_))

calcium = dict(zip(food_items,Calcium_))

iron = dict(zip(food_items,Iron_))

vit_E = dict(zip(food_items,VitaminE_))

Sugar = dict(zip(food_items,Sugar_))

costs = dict(zip(food_items,cost))



food_vars = LpVariable.dicts("Food name :",food_items,0,cat='Continuous')




prob = LpProblem("Simple Diet Problem",LpMinimize)





# The objective function is added to 'prob' first
prob += lpSum([vit_C[i]*food_vars[i] for i in food_items]), "Total Cost of the balanced diet"



prob += lpSum([calories[f] * food_vars[f] for f in food_items]) >= 20, "CalorieMinimum"
prob += lpSum([calories[f] * food_vars[f] for f in food_items]) <= 800, "CalorieMaximum"


# Fat
prob += lpSum([fat[f] * food_vars[f] for f in food_items]) >= 600, "FatMinimum"
prob += lpSum([fat[f] * food_vars[f] for f in food_items]) <= 900, "FatMaximum"

# Carbs
prob += lpSum([carbs[f] * food_vars[f] for f in food_items]) >= np.min(Carbohydrate_), "CarbsMinimum"
prob += lpSum([carbs[f] * food_vars[f] for f in food_items]) <= np.mean(Carbohydrate_), "CarbsMaximum"

# sugar
prob += lpSum([Sugar[f] * food_vars[f] for f in food_items]) >= np.min(Sugar_), "SugarMinimum"
prob += lpSum([Sugar[f] * food_vars[f] for f in food_items]) <= np.mean(Sugar_)-np.std(Sugar_), "SugarMaximum"

#Protein
prob += lpSum([protein[f] * food_vars[f] for f in food_items]) >= np.min(Protein_), "ProteinMinimum"
prob += lpSum([protein[f] * food_vars[f] for f in food_items]) <= np.mean(Protein_), "ProteinMaximum"







prob.writeLP("SimpleDietProblem.lp")
print(1)



prob.solve()



print("Status:", LpStatus[prob.status])



print("Therefore, the optimal (least cost) balanced diet consists of\n"+"-"*110)

food_data = []
c_Value = []
for v in prob.variables():
    if bool(v.varValue) != 0:
        if v.varValue > 0:
            print(v.name, "=", v.varValue)
            food_data += [v.name]
            c_Value += [v.varValue]
            
            
            
food_data = np.array(food_data)
print("YOUR foods  === ",food_data)


idx = np.argsort(c_Value)[::-1]
sorted_data = food_data[idx]
print(sorted_data[1:4])



c_Value_sort = np.sort(c_Value)
print(c_Value_sort) 




prob = []
prob = LpProblem("Simple Diet Problem min",LpMinimize)

prob += lpSum([costs[i]*food_vars[i] for i in food_items]), "Total Cost of the balanced diet"

prob += lpSum([calories[f] * food_vars[f] for f in food_items]) >= 20, "CalorieMinimum"
prob += lpSum([calories[f] * food_vars[f] for f in food_items]) <= 100, "CalorieMaximum"


# Fat
prob += lpSum([fat[f] * food_vars[f] for f in food_items]) >= 200, "FatMinimum"
prob += lpSum([fat[f] * food_vars[f] for f in food_items]) <= 500, "FatMaximum"

# Carbs
prob += lpSum([carbs[f] * food_vars[f] for f in food_items]) >= np.min(Carbohydrate_), "CarbsMinimum"
prob += lpSum([carbs[f] * food_vars[f] for f in food_items]) <= np.mean(Carbohydrate_), "CarbsMaximum"

# sugar
prob += lpSum([Sugar[f] * food_vars[f] for f in food_items]) >= np.min(Sugar_), "SugarMinimum"
prob += lpSum([Sugar[f] * food_vars[f] for f in food_items]) <= np.mean(Sugar_)-np.std(Sugar_), "SugarMaximum"

#Protein
prob += lpSum([protein[f] * food_vars[f] for f in food_items]) >= np.min(Protein_), "ProteinMinimum"
prob += lpSum([protein[f] * food_vars[f] for f in food_items]) <= np.mean(Protein_), "ProteinMaximum"
prob.writeLP("SimpleDietProblem.lp")
print(1)
prob.solve()
print("Status:", LpStatus[prob.status])
print("Therefore, the optimal (least cost) balanced diet consists of\n"+"-"*110)

food_data__2 = []
c_Value__2 = []
for v in prob.variables():
    if bool(v.varValue) != 0:
        if v.varValue > 0:
            print(v.name, "=", v.varValue)
            food_data__2 += [v.name]
            c_Value__2 += [v.varValue]


print("YOUR foods 2  === ",food_data__2)







