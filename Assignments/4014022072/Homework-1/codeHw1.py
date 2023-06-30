# get numbers

x = int(input('Enter number 1 : '))
y = int(input('Enter number 2 : '))


# count digits of numbers
def digit(n):
    count = 0
    if n <= 9:
        count = 1
    else:
        while n != 0:
            n //= 10
            count += 1
    return count


def Divide_Conquer(a, b):
    digita = digit(a)
    digitb = digit(b)
    digit_n = max(digitb, digita)
    # if one of numbers is 1 digit :
    if digit_n == 1:
        return a * b
    else:
        # Dividing numbers :
        aL = a // (10 ** (digit_n / 2))
        aR = a - (aL * (10 ** (digit_n / 2)))
        bL = b // (10 ** (digit_n / 2))
        bR = b - (bL * (10 ** (digit_n / 2)))
        # Calculation of the sub-problem
        x1 = Divide_Conquer(aL, bL)
        x2 = Divide_Conquer(aR, bR)
        x3 = Divide_Conquer(aL + aR, bL + bR)
        # Combine
        return (x1 * (10 ** digit_n)) + ((x3 - x1 - x2) * (10 ** (digit_n / 2))) + x2


z = int(Divide_Conquer(x, y))
print(z)
