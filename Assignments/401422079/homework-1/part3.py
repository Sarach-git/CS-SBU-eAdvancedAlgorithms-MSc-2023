#import the package we need
from math import ceil

# define the function for multiplication with divide and conquer strategy
def multiplication(X,Y):
    
    #simple solution 
    if X < 10 or Y < 10:
        
        return X*Y
    
    # Find the right value for division
    sizeMax =  max(len(str(X)) , len(str(Y)))
    
    n = ceil( sizeMax / 2 )
    
    #Dividing numbers
    a,b = splitFunction(X,n)
    
    c,d = splitFunction(Y,n)
    
    #Creating new subproblems
    ac = multiplication(a,c)
    
    bd = multiplication(b,d)
    
    adbc = multiplication(a+b , c+d) - ac - bd
    
    #Integration of subproblems
    returnValue = (ac * ( 10 ** (n*2))) + (adbc * ( 10 ** n)) + bd
    
    return returnValue

#This function divides numbers into two parts
def splitFunction(value , n):
    
    splitValue = 10 ** n
    
    leftPart = value // splitValue
    
    rightPart = value % splitValue
    
    return leftPart , rightPart


#test the code
x=5461527324789800
y=315346500
print(multiplication(x,y)==x*y)
print(multiplication(x,y))
