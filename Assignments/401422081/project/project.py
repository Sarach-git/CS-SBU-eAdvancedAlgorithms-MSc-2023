# Import all classes of PuLP module
from pulp import *
import pulp as pl
import warnings
warnings.simplefilter(action='ignore')
import pandas

userGender = 'm' #input('Are you male(m) or female(f)?')
userWeight = 80 #float(input('Please input your weight:'))
userActivity = '2' #input('Please input your daily activity from 1(office job or studying) to 3(labor or professional athlete)?')
userBodyFatPercentFactor = 0.95 #Average due to inability to measure
leanFactor = 0.9 #Average for the sake of simplicity
userGenderFactor = float(0.9 if userGender == 'f' else 1)
userActivityFactor = float(1.3 if userActivity == '1' else 1.65 if userActivity == '2' else 2)
userBMR = userWeight * userGenderFactor * 24 * userBodyFatPercentFactor 
userDailyCaloriesNeeded = userBMR * userActivityFactor
print(f'Your (Approximate) BMR is {userBMR} and you need {userDailyCaloriesNeeded} calories daily')
print(f'These are some foods you can take for today:')

problem = LpProblem('Diet Problem', LpMaximize)

x = [] #Initialize objective variables
xCoefficients = []

pandas.set_option('display.max_rows', None)
foods = pandas.read_csv('./USDA.csv') #fdc_id, description, food_category_id 
totalCalories = 0

cleanedData = []
for i in range(0,int(len(foods)/10)):
    foodId = foods.iloc[i]['ID']
    foodDescription = foods.iloc[i]['Description']
    calories = foods.iloc[i]['Calories']
    if(calories != 0):
        cleanedData.append({'ID': foodId, 'Description':foodDescription, 'Calories': calories})

print(len(cleanedData))
    

for i in range(0,len(cleanedData)):
    x.append(LpVariable(name= str(cleanedData[i]['ID']), upBound=1, lowBound=0, cat=LpInteger))
    xCoefficients.append(cleanedData[i]['Calories'])

problem += lpSum(x[i] * xCoefficients[i] for i in range(0, len(x)))
problem += lpSum(x[i] * xCoefficients[i] for i in range(0, len(x))) <= userDailyCaloriesNeeded

problem.solve()

for v in problem.variables():
    if(v.varValue == 1):
        # print(f'{v.name}')
        food = foods.query(f'ID == {v.name}')
        print(str(food['Description'].values) + '  ' + str(food['Calories'].values))