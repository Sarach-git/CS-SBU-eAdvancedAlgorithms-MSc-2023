# Import all classes of PuLP module
from pulp import *
import pulp as pl
import pandas


problem = LpProblem('Diet Problem', LpMaximize)

x = [] #Initialize objective variables
xCoefficients = []
# A = LpVariable('Car A', lowBound=0 , cat=LpInteger)
# B = LpVariable('Car B', lowBound=0 , cat=LpInteger)

# #Objective Function
# problem += 20000*A + 45000*B , 'Objective Function'
# #Constraints
# problem += 4*A + 5*B <= 30 , 'Designer Constraint'
# problem += 3*A + 6*B <=30, 'Engineer Constraint'
# problem += 2*A + 7*B <=30, 'Machine Constraint'


# #Objective Function
# problem += 20000*A + 45000*B , 'Objective Function'

pandas.set_option('display.max_rows', None)
df = pandas.read_csv('data.csv')
totalCalories = 0
for i in range(0,100):
    # print(df.iloc[i]['Calories'])
    totalCalories += df.iloc[i]['Calories']
    x.append(LpVariable(str( df.iloc[i]['ID']), range(1), cat=LpBinary))
    xCoefficients.append(df.iloc[i]['Calories'])
problem += lpSum(x[i] * xCoefficients[i] for i in range(0, len(x)))
print("Total calories: ", totalCalories) 
print("Current Status: ", LpStatus[problem.status]) 
problem.solve()
print("Objective: ", value(problem.objective))