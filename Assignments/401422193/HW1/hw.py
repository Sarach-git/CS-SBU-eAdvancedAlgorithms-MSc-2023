def multiplyxy(x,y):
    if len(str(x)) == 1 or len(str(y)) == 1:
        return x*y
    else:
        m = max(len(str(x)),len(str(y)))
        m2 = m // 2

        a = x // 10**(m2)
        b = x % 10**(m2)
        c = y // 10**(m2)
        d = y % 10**(m2)

        z0 = multiplyxy(b,d)
        z1 = multiplyxy((a+b),(c+d))
        z2 = multiplyxy(a,c)

        return (z2 * 10**(2*m2)) + ((z1 - z2 - z0) * 10**(m2)) + (z0)

print("What do you want to multiply? (Write 2 Whole/Integer Number)")
x1,x2=input("").split()
print(multiplyxy(int(x1),int(x2)))
