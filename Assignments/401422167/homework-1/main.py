import sys


def mul(a: str, b: str) -> str:
    # make the two input numbers the same length by adding zeros to the smaller one
    if len(a) < len(b):
        a = a.zfill(len(b))
    elif len(b) < len(a):
        b = b.zfill(len(a))

    # 1.let
    # n := number of digits
    n = len(a)
    # m := length of the left half (floor(n/2))
    l = n // 2
    # k := length of the right half (n - m)
    r = n - l

    # 2. if n == 1:
    if n == 1:
        # 3. return a * b
        return str(int(a) * int(b))

    # 4. let al and ar be the left and right halves of a               (divide)
    al, ar = a[:l], a[l:]

    # 5. let bl and br be the left and right halves of b               (divide)
    bl, br = b[:l], b[l:]

    # 6. let x be mul(al, bl)                                          (conquer)
    x = int(mul(al, bl))

    # 7. let y be mul(ar, br)                                          (conquer)
    y = int(mul(ar, br))

    # 8. let z be mul(al+ar, bl+br)                                    (conquer)
    z = int(mul(str(int(al) + int(ar)), str(int(bl) + int(br))))

    # 9. return x * 10 ** (2 * r) + (z - x - y) * 10 ** r + y          (combine)
    return str(x * 10 ** (2 * r) + (z - x - y) * 10 ** r + y)


def main():
    if len(sys.argv) != 3:
        print("this script needs exactly two arguments.")
        exit()

    a, b = sys.argv[1], sys.argv[2]

    print(mul(a, b))


if __name__ == "__main__":
    main()
