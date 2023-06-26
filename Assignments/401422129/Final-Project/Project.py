#MelikaAlikhaniRad #401422129
from pulp import LpProblem, LpVariable, lpSum, LpBinary, LpStatus, LpMaximize, CBC
import time

# Definingthedataset
dataset = {
    "Food": [
        "Egg",
        "Chicken Breast",
        "Salmon",
        "Spinach",
        "Mushrooms",
        "Onion",
        "Apple",
        "Carrot",
        "Almond Butter",
        "Brussels Sprouts",
        "Orange",
        "Banana",
        "Mixed Nuts",
        "Broccoli",
        "Sweet Potato",
    ],
    "Carbohydrate (g)": [
        1.1,
        0,
        0,
        1.1,
        0.3,
        0.9,
        13.8,
        10.5,
        3.5,
        8.9,
        15.4,
        22,
        13.5,
        7,
        20.7,
    ],
    "Fat (g)": [
        10,
        2,
        6,
        0.4,
        0.3,
        0.2,
        0.4,
        0.2,
        58,
        0.2,
        0.2,
        0.2,
        45.6,
        0.4,
        0.1,
    ],
    "Protein (g)": [
        12.6,
        23.5,
         19.6,
        2.9,
        3.1,
        1.2,
        0.3,
        0.9,
        21.1,
        3.4,
        1.1,
        1.3,
        14.2,
        2.8,
        2,
    ],
    "Calories": [
        143,
        165,
        206,
        23,
        22,
        40,
        52,
        41,
        614,
        43,
        43,
        96,
        607,
        55,
        90,
    ],
}


user_input = {
    "gender": "female",
    "calories": 2000,
}

problem = LpProblem("DietProblem", LpMaximize)

foods = dataset["Food"]
variables = LpVariable.dicts("Food", foods, lowBound=0, upBound=1, cat=LpBinary)

# Settheobjectivefunction(maximizevariety)
problem += lpSum([variables[food] for food in foods])

#constraints
problem += lpSum([dataset["Carbohydrate (g)"][i] * variables[food] for i, food in enumerate(foods)]) <= 40
problem += lpSum([dataset["Fat (g)"][i] * variables[food] for i, food in enumerate(foods)]) <= 165
problem += lpSum([dataset["Protein (g)"][i] * variables[food] for i, food in enumerate(foods)]) <= 75

# Addadditionalconstraintsbasedonuserinput
calorie_constraint = lpSum([dataset["Calories"][i] * variables[food] for i, food in enumerate(foods)]) <= user_input["calories"]
problem += calorie_constraint

# SolvetheproblemusingtheCBCsolver
start_time = time.time()
problem.solve(solver=CBC())
end_time = time.time()


print("Status:", LpStatus[problem.status])

# Printingtheoptimaldietplan
if problem.status == 1:
    print("Optimal Diet Plan:")
    for food in foods:
        if variables[food].value() > 0:
            print(food)
else:
    print("No solution found.")
