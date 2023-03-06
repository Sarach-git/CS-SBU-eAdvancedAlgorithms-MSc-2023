
def divide(a,b):
    ## The condition that stops the recursion, when one of the numbers is 1digits
    if(a%10 == a or b%10 == b):
        return a*b
        
    ## Finding digits of numbers, it is presumed that both numbers has the same lengh
    print('divide => a:' + str(a) + '    b: ' + str(b))
    digitsOfA = len(str(a))
    halfOfDigitsA = round(digitsOfA/2)

    ## Dividing numbers into 2 same size parts
    a1 = math.floor(a / (10**(halfOfDigitsA)))
    a0 = a % (10**(halfOfDigitsA))
    b1= math.floor(b / (10**(halfOfDigitsA)))
    b0 = b % (10**(halfOfDigitsA))

    ## Putting numbers into main formula, with recursion on multiplications
    c0=divide(a0,b0)
    c2=divide(a1,b1)
    c1=divide(a0+a1,b0+b1)-(c0+c2)
    result = c2*(10**digitsOfA) + c1*(10**halfOfDigitsA) + c0
    print('divide => result: ' + str(result))
    return result

print('result: ' + str(divide(1234,4321)))
print('result should be: ' + str(1234*4321))



