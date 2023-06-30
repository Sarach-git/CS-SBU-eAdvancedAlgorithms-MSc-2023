def get_length_of_digit(digit):
    return len(str(digit))


def multiply(x, y):
    x_length = get_length_of_digit(x)
    y_length = get_length_of_digit(y)

    # Conquer
    if x_length == 1 or y_length == 1:
        return x * y
    else:
        # Split
        n = max(x_length, y_length)
        m = n // 2

        xR = x // 10**m
        xL = x % 10**m
        yR = y // 10**m
        yL = y % 10**m

        # Combine
        z0 = multiply(xL, yL)
        z1 = multiply(xL + xR, yR + yL)
        z2 = multiply(xR, yR)

        return z2 * 10**(2*m) + (z1 - z2 - z0) * 10**m + z0