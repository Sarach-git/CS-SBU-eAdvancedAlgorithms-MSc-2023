# Import all classes of PuLP module
from pulp import *
import random
import pandas


# global vars :
sex = "female"
weight = 76
dailyActivityCount = 3
fatPercentage = 0.4
leanFactor = 0.8
sexFactor = 0
activityFactor = 0
bmr = 0
requiredCal = 0
total_cal = 0

# lists
my_list = []
my_coefficients = []
final_result = []
available_foods = []

linear_programming_problem = LpProblem('Diet',LpMaximize)

def calculateSexFactors():
    if(sex=="male"):
        return 0.9
    elif(sex=="female"):
        return 0.8
    else:
        return 0.0

def calculateActivityFactors():
    if(sex=="male"):
        return 1.5
    elif(sex=="female"):
        return 1.6
    else:
        return 0.0

def calculate_required_cal():
    global bmr
    global requiredCal
    bmr = weight * sexFactor * activityFactor
    requiredCal = bmr * activityFactor

def readData():
    pandas.set_option('display.max_rows',None)
    return pandas.read_csv('./USDA.csv')

def findCalories():
    global available_foods
    global final_result
    for i in range(int(len(available_foods)/10)):
        id = available_foods.iloc[i]['ID']
        description = available_foods.iloc[i]['Description']
        cal = available_foods.iloc[i]['Calories']
        if(cal != 0):
            temp = {'ID': id, 'Description':description, 'Calories': cal}
            final_result.append(temp)
            print(temp)

def find_daily_diet():
    global requiredCal
    global my_list
    global my_coefficients
    global linear_programming_problem
    global final_result
    for i in range(len(final_result)):
        my_list.append(LpVariable(name= str(final_result[i]['ID']), upBound=1, lowBound=0, cat=LpInteger))
        temp_cal = final_result[i]['Calories']
        my_coefficients.append(temp_cal)
    linear_programming_problem += lpSum(my_list[i] * my_coefficients[i] for i in range(len(my_list))) 
    linear_programming_problem += lpSum(my_list[i] * my_coefficients[i] for i in range(len(my_list))) <= requiredCal
    linear_programming_problem.solve()

def show_result():
    global linear_programming_problem
    for var in linear_programming_problem.variables():
        if(var.varValue == 1):
            food = available_foods.query(f'ID == {var.name}')
            amount = random.randint(1, 4) * 100
            print( str(amount) + "g of " + food['Description'].values + ' containing ' + str(food['Calories'].values * (amount/100)) + " calories")

def get_user_inputs():
    global sex
    global weight
    global dailyActivityCount
    sex = input('what is your sexuality?(type male or female)\n')
    weight = float(input('enter your weight:\n'))
    dailyActivityCount = float(input('enter your daily activity:\n'))

def main():
    global requiredCal
    global available_foods
    global sexFactor
    global activityFactor
    get_user_inputs()
    sexFactor = calculateSexFactors()
    activityFactor = calculateActivityFactors()
    calculate_required_cal()
    available_foods = readData()
    findCalories()
    find_daily_diet()
    show_result()

main()





