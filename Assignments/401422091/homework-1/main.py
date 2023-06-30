def multiplication(a, b):
    if len(a) < len(b):
        a, b = b, a
    if len(a) != len(b):
        while len(b) < len(a):
            b = f'0{b}'

    n = len(a)

    if n == 1:
        return int(a) * int(b)

    mid = int(n / 2)

    aR = a[-mid:]
    aL = a[:-mid]

    bR = b[-mid:]
    bL = b[:-mid]

    x1 = int(multiplication(aL, bL))
    x2 = int(multiplication(aR, bR))
    x3 = int(multiplication(str(int(aL) + int(aR)), str(int(bL) + int(bR))))

    return (x1 * (10 ** (mid * 2))) + ((x3 - x1 - x2) * (10 ** mid)) + x2

print('Our function returns: ',multiplication('23432455', '655578'))
print('Actual multiplication by of returns: ',23432455 * 655578)
