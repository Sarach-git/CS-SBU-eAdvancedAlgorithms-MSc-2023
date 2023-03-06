def karatsuba(m, n):
    # Base condition
    if m < 10 or n < 10:
        return m * n
    else:
        # Finding n/2
        k = max(len(str(m)), len(str(n)))
        mid = int(k / 2)

        # Finding a,b,c and d
        a = m // 10**(mid)
        b = m % 10**(mid)
        c = n // 10**(mid)
        d = n % 10**(mid)

        # Finding ac, bd and ad_plus_bc
        ac = karatsuba(a, c)
        bd = karatsuba(b, d)
        ad_plus_bc = karatsuba(a + b, c + d) - ac - bd

        # Result
        return ac * 10**(2 * mid) + ad_plus_bc * 10**(mid) + bd


print(karatsuba(23958233, 5830))
